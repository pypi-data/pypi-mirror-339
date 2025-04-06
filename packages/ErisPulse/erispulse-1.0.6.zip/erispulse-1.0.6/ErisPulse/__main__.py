import argparse
import os
import sys
import shutil
import aiohttp
import zipfile
import asyncio
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import track
from .envManager import env
from .origin import origin_manager

console = Console()

def enable_module(module_name):
    module_info = env.get_module(module_name)
    if module_info:
        env.set_module_status(module_name, True)
        console.print(f"[green]模块 {module_name} 已启用[/green]")
    else:
        console.print(f"[red]模块 {module_name} 不存在[/red]")

def disable_module(module_name):
    module_info = env.get_module(module_name)
    if module_info:
        env.set_module_status(module_name, False)
        console.print(f"[yellow]模块 {module_name} 已禁用[/yellow]")
    else:
        console.print(f"[red]模块 {module_name} 不存在[/red]")

async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        console.print(f"[red]请求失败: {e}[/red]")
        return None

def extract_and_setup_module(module_name, module_url, zip_path, module_dir):
    try:
        console.print(f"[cyan]正在从 {module_url} 下载模块...[/cyan]")
        
        async def download_module():
            async with aiohttp.ClientSession() as session:
                content = await fetch_url(session, module_url)
                if content is None:
                    return False
                
                with open(zip_path, 'wb') as zip_file:
                    zip_file.write(content)

                if not os.path.exists(module_dir):
                    os.makedirs(module_dir)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(module_dir)
                
                init_file_path = os.path.join(module_dir, '__init__.py')
                if not os.path.exists(init_file_path):
                    sub_module_dir = os.path.join(module_dir, module_name)
                    m_sub_module_dir = os.path.join(module_dir, f"m_{module_name}")
                    for sub_dir in [sub_module_dir, m_sub_module_dir]:
                        if os.path.exists(sub_dir) and os.path.isdir(sub_dir):
                            for item in os.listdir(sub_dir):
                                source_item = os.path.join(sub_dir, item)
                                target_item = os.path.join(module_dir, item)
                                if os.path.exists(target_item):
                                    os.remove(target_item)
                                shutil.move(source_item, module_dir)
                            os.rmdir(sub_dir)

                console.print(f"[green]模块 {module_name} 文件已成功解压并设置[/green]")
                return True
        
        return asyncio.run(download_module())

    except Exception as e:
        console.print(Panel(f"[red]处理模块 {module_name} 文件失败: {e}[/red]", title="错误", border_style="red"))
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except Exception as cleanup_error:
                console.print(f"[red]清理失败: {cleanup_error}[/red]")
        return False

    finally:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except Exception as cleanup_error:
                console.print(f"[red]清理失败: {cleanup_error}[/red]")

def install_pip_dependencies(dependencies):
    if not dependencies:
        return True

    console.print("[cyan]正在安装pip依赖...[/cyan]")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install"] + dependencies,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        console.print(result.stdout.decode())
        return True
    except subprocess.CalledProcessError as e:
        console.print(Panel(f"[red]安装pip依赖失败: {e.stderr.decode()}[/red]", title="错误", border_style="red"))
        return False

def install_module(module_name, force=False):
    module_info = env.get_module(module_name)
    if module_info and not force:
        console.print(f"[yellow]模块 {module_name} 已存在，使用 --force 参数强制重装[/yellow]")
        return

    providers = env.get('providers', {})
    if isinstance(providers, str):
        providers = json.loads(providers)

    module_info = []
    for provider, url in providers.items():
        module_key = f"{module_name}@{provider}"
        modules_data = env.get('modules', {})
        if isinstance(modules_data, str):
            modules_data = json.loads(modules_data)

        if module_key in modules_data:
            module_data = modules_data[module_key]
            module_info.append({
                'provider': provider,
                'url': url,
                'path': module_data.get('path', ''),
                'version': module_data.get('version', '未知'),
                'description': module_data.get('description', '无描述'),
                'author': module_data.get('author', '未知'),
                'dependencies': module_data.get('dependencies', []),
                'optional_dependencies': module_data.get('optional_dependencies', []),
                'pip_dependencies': module_data.get('pip_dependencies', [])
            })

    if not module_info:
        console.print(f"[red]未找到模块 {module_name}[/red]")
        return

    if len(module_info) > 1:
        console.print(f"[cyan]找到 {len(module_info)} 个源的 {module_name} 模块：[/cyan]")
        table = Table(title="可选模块源", show_header=True, header_style="bold magenta")
        table.add_column("编号", style="cyan")
        table.add_column("源", style="green")
        table.add_column("版本", style="blue")
        table.add_column("描述", style="white")
        table.add_column("作者", style="yellow")
        for i, info in enumerate(module_info):
            table.add_row(str(i+1), info['provider'], info['version'], info['description'], info['author'])
        console.print(table)

        while True:
            choice = Prompt.ask("请选择要安装的源 (输入编号)", default="1")
            if choice.isdigit() and 1 <= int(choice) <= len(module_info):
                selected_module = module_info[int(choice)-1]
                break
            else:
                console.print("[red]输入无效，请重新选择[/red]")
    else:
        selected_module = module_info[0]

    for dep in selected_module['dependencies']:
        console.print(f"[cyan]正在安装依赖模块 {dep}...[/cyan]")
        install_module(dep)

    third_party_deps = selected_module.get('pip_dependencies', [])
    if third_party_deps:
        console.print(f"[cyan]模块 {module_name} 需要以下pip依赖: {', '.join(third_party_deps)}[/cyan]")
        if not install_pip_dependencies(third_party_deps):
            console.print(f"[red]无法安装模块 {module_name} 的pip依赖，安装终止[/red]")
            return
    
    module_url = selected_module['url'] + selected_module['path']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.join(script_dir, 'modules', module_name)
    zip_path = os.path.join(script_dir, f"{module_name}.zip")

    if not extract_and_setup_module(
        module_name=module_name,
        module_url=module_url,
        zip_path=zip_path,
        module_dir=module_dir
    ):
        return

    env.set_module(module_name, {
        'status': True,
        'info': {
            'version': selected_module['version'],
            'description': selected_module['description'],
            'author': selected_module['author'],
            'dependencies': selected_module['dependencies'],
            'optional_dependencies': selected_module['optional_dependencies'],
            'pip_dependencies': selected_module['pip_dependencies']
        }
    })
    console.print(f"[green]模块 {module_name} 安装成功[/green]")

def uninstall_module(module_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(script_dir, 'modules', module_name)

    module_file_path = module_path + '.py'
    if os.path.exists(module_file_path):
        try:
            os.remove(module_file_path)
        except Exception as e:
            console.print(f"[red]删除模块文件 {module_name} 时出错: {e}[/red]")
    elif os.path.exists(module_path) and os.path.isdir(module_path):
        try:
            shutil.rmtree(module_path)
        except Exception as e:
            console.print(f"[red]删除模块目录 {module_name} 时出错: {e}[/red]")
    else:
        console.print(f"[red]模块 {module_name} 不存在[/red]")
        return
    
    module_info = env.get_module(module_name)
    if not module_info:
        console.print(f"[red]模块 {module_name} 不存在[/red]")
        return
    
    pip_dependencies = module_info.get('info', {}).get('pip_dependencies', [])
    if pip_dependencies:
        all_modules = env.get_all_modules()
        unused_pip_dependencies = []
        
        essential_packages = {'aiohttp', 'rich'}

        for dep in pip_dependencies:
            if dep in essential_packages:
                console.print(f"[yellow]跳过必要模块 {dep} 的卸载[/yellow]")
                continue

            is_dependency_used = False
            for name, info in all_modules.items():
                if name != module_name and dep in info.get('info', {}).get('pip_dependencies', []):
                    is_dependency_used = True
                    break
            if not is_dependency_used:
                unused_pip_dependencies.append(dep)
        
        if unused_pip_dependencies:
            console.print(f"[cyan]以下 pip 依赖不再被其他模块使用: {', '.join(unused_pip_dependencies)}[/cyan]")
            confirm = Confirm.ask("[yellow]是否卸载这些 pip 依赖？[/yellow]", default=False)
            if confirm:
                console.print(f"[cyan]正在卸载 pip 依赖: {', '.join(unused_pip_dependencies)}[/cyan]")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "uninstall", "-y"] + unused_pip_dependencies,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    console.print(f"[green]成功卸载 pip 依赖: {', '.join(unused_pip_dependencies)}[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(Panel(f"[red]卸载 pip 依赖失败: {e.stderr.decode()}[/red]", title="错误", border_style="red"))
    
    if env.remove_module(module_name):
        console.print(f"[green]模块 {module_name} 已删除[/green]")
    else:
        console.print(f"[red]模块 {module_name} 不存在[/red]")
def upgrade_all_modules(force=False):
    all_modules = env.get_all_modules()
    if not all_modules:
        console.print("[yellow]未找到任何模块，无法更新[/yellow]")
        return

    providers = env.get('providers', {})
    if isinstance(providers, str):
        providers = json.loads(providers)

    modules_data = env.get('modules', {})
    if isinstance(modules_data, str):
        modules_data = json.loads(modules_data)

    updates_available = []
    for module_name, module_info in all_modules.items():
        local_version = module_info['info'].get('version', '0.0.0')
        for provider, url in providers.items():
            module_key = f"{module_name}@{provider}"
            if module_key in modules_data:
                remote_module = modules_data[module_key]
                remote_version = remote_module.get('version', '0.0.0')
                if remote_version > local_version:
                    updates_available.append({
                        'name': module_name,
                        'local_version': local_version,
                        'remote_version': remote_version,
                        'provider': provider,
                        'url': url,
                        'path': remote_module.get('path', ''),
                    })

    if not updates_available:
        console.print("[green]所有模块已是最新版本，无需更新[/green]")
        return

    console.print("\n[cyan]以下模块有可用更新：[/cyan]")
    table = Table(title="可用更新", show_header=True, header_style="bold magenta")
    table.add_column("模块", style="cyan")
    table.add_column("当前版本", style="yellow")
    table.add_column("最新版本", style="green")
    table.add_column("源", style="blue")
    for update in updates_available:
        table.add_row(update['name'], update['local_version'], update['remote_version'], update['provider'])
    console.print(table)

    if not force:
        confirm = Confirm.ask("[yellow]警告：更新模块可能会导致兼容性问题，请在更新前查看插件作者的相关声明。\n是否继续？[/yellow]", default=False)
        if not confirm:
            console.print("[yellow]更新已取消[/yellow]")
            return

    for update in updates_available:
        console.print(f"[cyan]正在更新模块 {update['name']}...[/cyan]")
        module_url = update['url'] + update['path']
        script_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.join(script_dir, 'modules', update['name'])
        zip_path = os.path.join(script_dir, f"{update['name']}.zip")

        if not extract_and_setup_module(
            module_name=update['name'],
            module_url=module_url,
            zip_path=zip_path,
            module_dir=module_dir
        ):
            continue

        all_modules[update['name']]['info']['version'] = update['remote_version']
        env.set_all_modules(all_modules)
        console.print(f"[green]模块 {update['name']} 已更新至版本 {update['remote_version']}[/green]")

def list_modules(module_name=None):
    all_modules = env.get_all_modules()
    if not all_modules:
        console.print("[yellow]未在数据库中发现注册模块,正在初始化模块列表...[/yellow]")
        from . import init as init_module
        init_module()
        all_modules = env.get_all_modules()

    if not all_modules:
        console.print("[red]未找到任何模块[/red]")
        return

    table = Table(title="模块列表", show_header=True, header_style="bold magenta")
    table.add_column("模块名称", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("版本", style="blue")
    table.add_column("描述", style="white")
    table.add_column("依赖", style="yellow")
    table.add_column("可选依赖", style="magenta")
    table.add_column("pip依赖", style="cyan")

    for name, info in all_modules.items():
        status = "启用" if info.get("status", True) else "禁用"
        dependencies = ', '.join(info['info'].get('dependencies', [])) if info['info'].get('dependencies') else '无'
        optional_dependencies = ', '.join(info['info'].get('optional_dependencies', [])) if info['info'].get('optional_dependencies') else '无'
        pip_dependencies = ', '.join(info['info'].get('pip_dependencies', [])) if info['info'].get('pip_dependencies') else '无'
        table.add_row(
            name,
            status,
            info['info'].get('version', '未知'),
            info['info'].get('description', '无描述'),
            dependencies,
            optional_dependencies,
            pip_dependencies
        )

    console.print(table)

def main():
    parser = argparse.ArgumentParser(
        description="ErisPulse 命令行工具",
        prog="python -m ErisPulse"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    enable_parser = subparsers.add_parser('enable', help='启用指定模块')
    enable_parser.add_argument('module_name', type=str, help='要启用的模块名称')
    enable_parser.add_argument('--init', action='store_true', help='在启用模块前初始化模块数据库')

    disable_parser = subparsers.add_parser('disable', help='禁用指定模块')
    disable_parser.add_argument('module_name', type=str, help='要禁用的模块名称')
    disable_parser.add_argument('--init', action='store_true', help='在禁用模块前初始化模块数据库')

    list_parser = subparsers.add_parser('list', help='列出所有模块信息')
    list_parser.add_argument('--module', '-m', type=str, help='指定要展示的模块名称')

    update_parser = subparsers.add_parser('update', help='更新模块列表')

    upgrade_parser = subparsers.add_parser('upgrade', help='升级模块列表')
    upgrade_parser.add_argument('--force', action='store_true', help='跳过二次确认，强制更新')

    uninstall_parser = subparsers.add_parser('uninstall', help='删除指定模块')
    uninstall_parser.add_argument('module_name', type=str, help='要删除的模块名称')

    install_parser = subparsers.add_parser('install', help='安装指定模块（支持多个模块，用逗号分隔）')
    install_parser.add_argument('module_name', type=str, help='要安装的模块名称')
    install_parser.add_argument('--force', action='store_true', help='强制重新安装模块')
    install_parser.add_argument('--init', action='store_true', help='在安装模块前初始化模块数据库')

    origin_parser = subparsers.add_parser('origin', help='管理模块源')
    origin_subparsers = origin_parser.add_subparsers(dest='origin_command', help='源管理命令')

    add_origin_parser = origin_subparsers.add_parser('add', help='添加模块源')
    add_origin_parser.add_argument('url', type=str, help='要添加的模块源URL')

    list_origin_parser = origin_subparsers.add_parser('list', help='列出所有模块源')

    del_origin_parser = origin_subparsers.add_parser('del', help='删除模块源')
    del_origin_parser.add_argument('url', type=str, help='要删除的模块源URL')

    args = parser.parse_args()

    if hasattr(args, 'init') and args.init:
        console.print("[yellow]正在初始化模块列表...[/yellow]")
        from . import init as init_module
        init_module()

    # 全部指令：enable, disable, list, uninstall, install, update, origin(add, list, del)
    if args.command == 'enable':
        enable_module(args.module_name)
    elif args.command == 'disable':
        disable_module(args.module_name)
    elif args.command == 'list':
        list_modules(args.module)
    elif args.command == 'uninstall':
        uninstall_module(args.module_name)
    elif args.command == 'install':
        module_names = args.module_name.split(',')
        for module_name in module_names:
            module_name = module_name.strip()
            if module_name:
                install_module(module_name, args.force)
    elif args.command == 'update':
        origin_manager.update_origins()
    elif args.command == 'upgrade':
        upgrade_all_modules(args.force)
    elif args.command == 'origin':
        if args.origin_command == 'add':
            origin_manager.add_origin(args.url)
        elif args.origin_command == 'list':
            origin_manager.list_origins()
        elif args.origin_command == 'del':
            origin_manager.del_origin(args.url)
        else:
            origin_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()