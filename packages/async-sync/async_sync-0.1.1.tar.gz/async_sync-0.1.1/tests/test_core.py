"""
测试 async-sync 核心功能
Test async-sync core functionality
"""

import asyncio
import time
import unittest

import async_sync


class TestCore(unittest.TestCase):
    def test_run_async_in_sync(self):
        """测试在同步上下文中运行异步函数"""

        async def async_add(a, b):
            await asyncio.sleep(0.1)
            return a + b

        # 在同步代码中运行异步函数
        result = async_sync.run_async_in_sync(async_add(1, 2))
        self.assertEqual(result, 3)

    def test_run_sync_in_async(self):
        """测试在异步上下文中运行同步函数"""

        def sync_add(a, b):
            time.sleep(0.1)
            return a + b

        async def test():
            # 在异步代码中运行同步函数
            result = await async_sync.run_sync_in_async(sync_add, 1, 2)
            self.assertEqual(result, 3)

        asyncio.run(test())

    def test_sync_decorator(self):
        """测试 @to_sync 装饰器"""

        @async_sync.to_sync
        async def async_add(a, b):
            await asyncio.sleep(0.1)
            return a + b

        # 现在 async_add 可以在同步代码中直接调用
        result = async_add(1, 2)
        self.assertEqual(result, 3)

        # 也可以在异步代码中调用
        async def test():
            result = async_add(3, 4)
            self.assertEqual(result, 7)

        asyncio.run(test())

    def test_async_decorator(self):
        """测试 @to_async 装饰器"""

        def sync_add(a, b):
            time.sleep(0.1)
            return a + b

        async_add = async_sync.to_async(sync_add)

        # 在异步代码中调用装饰后的函数
        async def test():
            result = await async_add(1, 2)
            self.assertEqual(result, 3)

        asyncio.run(test())

    def test_nested_event_loop(self):
        """测试嵌套事件循环场景"""

        @async_sync.to_sync
        async def outer_func():
            await asyncio.sleep(0.1)

            @async_sync.to_sync
            async def inner_func():
                await asyncio.sleep(0.1)
                return "inner"

            # 在异步函数内调用同步化的异步函数
            result = inner_func()
            return f"outer-{result}"

        # 在同步代码中调用
        result = outer_func()
        self.assertEqual(result, "outer-inner")


if __name__ == "__main__":
    unittest.main()
