# ErisPulse

本项目基于 [RyhBotPythonSDK V2](https://github.com/runoneall/RyhBotPythonSDK2) 构建，并由 [sdkFrame](https://github.com/runoneall/sdkFrame) 提供支持。这是一个异步版本的 SDK，可能在功能和特性上与原库存在一定差异。

ErisPulse 是一个模块化、可扩展的异步 Python SDK 框架，主要用于构建高效、可维护的机器人应用程序。

# 更新日志
## 1.0.4
修复了部分命令行不支持logger颜色代码的问题 | 替换为rich

## 1.0.5
更新了SDK 模块对于pip依赖安装的支持

## 1.0.6
修复了SDK-CLI中的颜色乱码问题,并将db调整为包内存储,以解决多进程问题