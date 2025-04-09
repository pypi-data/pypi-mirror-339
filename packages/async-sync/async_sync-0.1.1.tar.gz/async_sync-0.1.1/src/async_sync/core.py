import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any, Callable, TypeVar, ParamSpec, Coroutine

import functools
import typing


T = TypeVar("T")
P = ParamSpec("P")


def run_async_in_sync(coro: Coroutine[Any, Any, T]) -> T:
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


async def run_sync_in_async(
    func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
) -> T:
    """
    在异步环境中安全地运行同步函数。
    Safely run sync functions in an asynchronous environment.

    参数/Parameters:
        func: 要运行的同步函数
        func: The synchronous function to run
        *args: 传递给函数的位置参数
        *args: Positional arguments to pass to the function
        **kwargs: 传递给函数的关键字参数
        **kwargs: Keyword arguments to pass to the function

    返回/Returns:
        函数的执行结果
        The execution result of the function
    """
    return await asyncio.to_thread(func, *args, **kwargs)


def is_async_callable(obj: typing.Any) -> bool:
    """
    检查对象是否是一个异步可调用对象。
    Check if an object is an async callable.

    参数/Parameters:
        obj: 要检查的对象
        obj: The object to check

    参考/Reference:
        https://github.com/encode/starlette/blob/0.46.1/starlette/_utils.py#L35-L39
    """
    while isinstance(obj, functools.partial):
        obj = obj.func

    return asyncio.iscoroutinefunction(obj) or (
        callable(obj) and asyncio.iscoroutinefunction(obj.__call__)  # type: ignore
    )


def to_sync(async_func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, T]:
    """
    将异步函数转换为同步函数的装饰器。
    Decorator to convert an async function to a sync function.

    参数/Parameters:
        async_func: 要转换的异步函数
        async_func: The async function to convert

    返回/Returns:
        转换后的同步函数
        The converted sync function
    """
    if not is_async_callable(async_func):
        raise ValueError("The provided function is not an async function.")

    @wraps(async_func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return run_async_in_sync(async_func(*args, **kwargs))

    return wrapper


def to_async(sync_func: Callable[P, T]) -> Callable[P, Coroutine[Any, Any, T]]:
    """
    将同步函数转换为异步函数的装饰器。
    Decorator to convert a sync function to an async function.

    参数/Parameters:
        sync_func: 要转换的同步函数
        sync_func: The sync function to convert

    返回/Returns:
        转换后的异步函数
        The converted async function
    """
    if is_async_callable(sync_func):
        raise ValueError("The provided function is not a sync function.")

    @wraps(sync_func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return await run_sync_in_async(sync_func, *args, **kwargs)

    return wrapper
