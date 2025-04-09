"""
async-sync - 优雅地在Python同步和异步代码之间转换
async-sync - Elegant conversion between Python sync and async code
"""

from .core import to_async, run_async_in_sync, run_sync_in_async, to_sync

# 添加别名以支持测试中使用的名称
sync = to_sync
async_ = to_async

__all__ = [
    "to_async",
    "run_async_in_sync",
    "run_sync_in_async",
    "to_sync",
    "sync",
    "async_",
]

__version__ = "0.1.0"
