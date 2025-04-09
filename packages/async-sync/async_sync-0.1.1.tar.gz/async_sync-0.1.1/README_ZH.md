# async-sync

[English Documentation](README.md)

[![PyPI version](https://img.shields.io/pypi/v/async-sync.svg)](https://pypi.org/project/async-sync/)
[![Python Version](https://img.shields.io/pypi/pyversions/async-sync.svg)](https://pypi.org/project/async-sync/)
[![License](https://img.shields.io/github/license/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/async-sync)](https://pepy.tech/project/async-sync)
[![GitHub Stars](https://img.shields.io/github/stars/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/issues)
[![Dependencies](https://img.shields.io/librariesio/github/Haskely/async-sync)](https://libraries.io/github/Haskely/async-sync)

-----

**async-sync** —— 优雅地在 Python 同步和异步代码之间转换

## 特性

- ✨ 简单易用的 API
- 🔄 在同步代码中无缝调用异步函数
- 🔄 在异步代码中无缝调用同步函数
- 🧠 智能处理嵌套事件循环
- 🛡️ 类型提示完备
- 📦 无外部依赖

## 安装

```sh
pip install async-sync
```

## 使用示例

### 将异步函数转换为同步函数

```python
import async_sync
import asyncio

@async_sync.to_sync
async def synced_func():
    await asyncio.sleep(1)
    return "Hello from async world!"

# 可以在同步代码中直接调用
print(synced_func())  # 输出：Hello from async world!

# 也可以在异步代码中调用
async def main():
    print(synced_func())  # 仍然正常工作

asyncio.run(main())
```

### 将同步函数转换为异步函数

```python
import async_sync
import time

def blocking_func(name):
    time.sleep(1)  # 模拟耗时操作
    return f"Hello, {name}!"

# 将同步函数转换为异步函数
async_hello = async_sync.to_async(blocking_func)

# 在异步代码中调用
import asyncio

async def main():
    # 可以用 await 调用
    result = await async_hello("World")
    print(result)  # 输出：Hello, World!

    # 可以并发调用多个
    results = await asyncio.gather(
        async_hello("Alice"),
        async_hello("Bob"),
        async_hello("Charlie")
    )
    print(results)  # 输出：['Hello, Alice!', 'Hello, Bob!', 'Hello, Charlie!']

asyncio.run(main())
```

### 直接运行协程或同步函数

```python
import async_sync
import asyncio
import time

# 在同步代码中运行协程
async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"

data = async_sync.run_async_in_sync(fetch_data())
print(data)  # 输出：Data fetched

# 在异步代码中运行同步函数
async def main():
    def cpu_intensive_task():
        time.sleep(1)  # 模拟CPU密集型任务
        return "Task completed"

    result = await async_sync.run_sync_in_async(cpu_intensive_task)
    print(result)  # 输出：Task completed

asyncio.run(main())
```

## 开发

### 安装依赖

```bash
uv sync
```

### 运行测试

```bash
uv run pytest
```

### commit

```bash
pre-commit install
cz commit
```

### 发布

```bash
cz bump

git push --follow-tags
```
