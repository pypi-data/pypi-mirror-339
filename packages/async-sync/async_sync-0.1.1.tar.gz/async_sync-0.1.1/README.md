# async-sync

[中文文档](README_ZH.md)

[![PyPI version](https://img.shields.io/pypi/v/async-sync.svg)](https://pypi.org/project/async-sync/)
[![Python Version](https://img.shields.io/pypi/pyversions/async-sync.svg)](https://pypi.org/project/async-sync/)
[![License](https://img.shields.io/github/license/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/async-sync)](https://pepy.tech/project/async-sync)
[![GitHub Stars](https://img.shields.io/github/stars/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Haskely/async-sync.svg)](https://github.com/Haskely/async-sync/issues)
[![Dependencies](https://img.shields.io/librariesio/github/Haskely/async-sync)](https://libraries.io/github/Haskely/async-sync)

-----

**async-sync** — Elegantly convert between Python synchronous and asynchronous code

## Features

- ✨ Simple and easy-to-use API
- 🔄 Seamlessly call async functions in synchronous code
- 🔄 Seamlessly call synchronous functions in async code
- 🧠 Intelligent handling of nested event loops
- 🛡️ Comprehensive type hints
- 📦 No external dependencies

## Installation

```sh
pip install async-sync
```

## Usage Examples

### Convert async functions to sync functions

```python
import async_sync
import asyncio

@async_sync.to_sync
async def synced_func():
    await asyncio.sleep(1)
    return "Hello from async world!"

# Can be called directly in synchronous code
print(synced_func())  # Output: Hello from async world!

# Also works in async code
async def main():
    print(synced_func())  # Still works normally

asyncio.run(main())
```

### Convert sync functions to async functions

```python
import async_sync
import time

def blocking_func(name):
    time.sleep(1)  # Simulate time-consuming operation
    return f"Hello, {name}!"

# Convert synchronous function to asynchronous
async_hello = async_sync.to_async(blocking_func)

# Use in async code
import asyncio

async def main():
    # Can be called with await
    result = await async_hello("World")
    print(result)  # Output: Hello, World!

    # Can be called concurrently
    results = await asyncio.gather(
        async_hello("Alice"),
        async_hello("Bob"),
        async_hello("Charlie")
    )
    print(results)  # Output: ['Hello, Alice!', 'Hello, Bob!', 'Hello, Charlie!']

asyncio.run(main())
```

### Directly run coroutines or sync functions

```python
import async_sync
import asyncio
import time

# Run coroutines in synchronous code
async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"

data = async_sync.run_async_in_sync(fetch_data())
print(data)  # Output: Data fetched

# Run synchronous functions in async code
async def main():
    def cpu_intensive_task():
        time.sleep(1)  # Simulate CPU-intensive task
        return "Task completed"

    result = await async_sync.run_sync_in_async(cpu_intensive_task)
    print(result)  # Output: Task completed

asyncio.run(main())
```

## Development

### Install dependencies

```bash
uv sync
```

### Run tests

```bash
uv run pytest
```

### Commit

```bash
pre-commit install
cz commit
```

### Release

```bash
cz bump

git push --follow-tags
```
