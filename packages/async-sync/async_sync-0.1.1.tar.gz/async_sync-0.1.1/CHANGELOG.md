# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.1.1 (2025-04-09)

### Refactor

- remove sync and async_ aliases from __init__.py

## v0.1.0 (2025-04-09)

### Feat

- 初始版本发布
- 核心功能实现
  - `run_async_in_sync` 函数 (从同步代码调用异步函数)
  - `run_sync_in_async` 函数 (从异步代码调用同步函数)
  - `@to_sync` 装饰器 (将异步函数转换为同步函数)
  - `@to_async` 装饰器 (将同步函数转换为异步函数)
- 完整的单元测试、集成测试和边缘情况测试
- 详细的文档和使用示例
