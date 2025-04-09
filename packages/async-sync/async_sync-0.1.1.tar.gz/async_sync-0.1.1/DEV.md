核心用法

```python
import async_sync
import asyncio

@async_sync.to_sync
async def synced_func():
    await asyncio.sleep(1)
    return "async_func"

# works in sync code
print(synced_func())

# also works in event loop
async def main():
    print(synced_func())
asyncio.run(main())

```

核心逻辑

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def run_async_in_sync(coro):
    """
    在同步环境中安全地运行异步协程，无论当前是否已在异步上下文中。
    Safely run async coroutines in a synchronous environment, regardless of whether there's an existing async context.

    参数/Parameters:
        coro: 要运行的异步协程对象
        coro: The async coroutine object to run

    返回/Returns:
        协程的执行结果
        The execution result of the coroutine

    说明/Notes:
        - 在没有运行中的事件循环时，直接使用 asyncio.run 执行协程
        - 在已有事件循环运行时，使用线程池在新线程中执行协程

        - When no event loop is running, directly use asyncio.run to execute the coroutine
        - When an event loop is already running, use thread pool to execute in a new thread
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        # 没有运行中的事件循环，直接使用 asyncio.run
        # No running event loop, directly use asyncio.run
        return asyncio.run(coro)
    else:
        # 已经处在一个事件循环中，使用线程池在新线程中运行
        # Already in an event loop, use thread pool to run in a new thread
        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(asyncio.run, coro).result()
```

```python

async def run_sync_in_async(func, *args, **kwargs):
    """
    在异步环境中安全地运行同步函数，无论当前是否已在同步上下文中。
    Safely run sync functions in an asynchronous environment, regardless of whether there's an existing sync context.
    """
    return await asyncio.to_thread(func, *args, **kwargs)
