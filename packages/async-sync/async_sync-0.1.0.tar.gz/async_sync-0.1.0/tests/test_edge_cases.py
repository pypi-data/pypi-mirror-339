"""
测试 async-sync 边缘情况
Test async-sync edge cases
"""

import asyncio
import time
import unittest
import threading

import async_sync


class TestEdgeCases(unittest.TestCase):
    def test_recursive_calls(self):
        """测试递归调用场景"""

        def sync_factorial(n):
            if n <= 1:
                return 1
            return n * sync_factorial(n - 1)

        async_factorial = async_sync.to_async(sync_factorial)

        async def test():
            # 测试异步调用递归同步函数
            result = await async_factorial(5)
            self.assertEqual(result, 120)

        asyncio.run(test())

    def test_nested_decorators(self):
        """测试嵌套装饰器场景"""

        def other_decorator(func):
            async def async_wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                return result + 1

            return async_wrapper

        @async_sync.to_sync
        @other_decorator
        async def nested_func(x):
            await asyncio.sleep(0.1)
            return x * 2

        # 装饰器顺序: to_sync(other_decorator(nested_func))
        # 预期结果: (x*2) + 1
        result = nested_func(5)
        self.assertEqual(result, 11)

    def test_timeout_handling(self):
        """测试超时处理"""

        def slow_sync_func():
            time.sleep(1.0)
            return "done"

        async def run_with_timeout():
            try:
                # 设置 0.5 秒超时
                _ = await asyncio.wait_for(
                    async_sync.run_sync_in_async(slow_sync_func), timeout=0.5
                )
                self.fail("应该超时但没有")
            except asyncio.TimeoutError:
                return "timeout_occurred"

        result = asyncio.run(run_with_timeout())
        self.assertEqual(result, "timeout_occurred")

    def test_exception_propagation(self):
        """测试异常传播"""

        class CustomException(Exception):
            pass

        def sync_raises_custom():
            raise CustomException("Custom sync exception")

        async def async_raises_custom():
            await asyncio.sleep(0.1)
            raise CustomException("Custom async exception")

        # 测试同步到异步的异常传播
        async def test_sync_to_async():
            with self.assertRaises(CustomException) as cm:
                await async_sync.run_sync_in_async(sync_raises_custom)
            self.assertIn("Custom sync exception", str(cm.exception))

        asyncio.run(test_sync_to_async())

        # 测试异步到同步的异常传播
        with self.assertRaises(CustomException) as cm:
            async_sync.run_async_in_sync(async_raises_custom())
        self.assertIn("Custom async exception", str(cm.exception))

    def test_thread_safety(self):
        """测试线程安全性"""
        counter = 0
        lock = threading.Lock()

        def increment_counter():
            nonlocal counter
            with lock:
                current = counter
                time.sleep(0.01)  # 强制线程切换
                counter = current + 1
            return counter

        async def run_concurrent_increments():
            async_increment = async_sync.to_async(increment_counter)
            tasks = [async_increment() for _ in range(10)]
            results = await asyncio.gather(*tasks)
            return results

        # 执行并发增量操作
        results = async_sync.run_async_in_sync(run_concurrent_increments())

        # 验证最终计数器值
        self.assertEqual(counter, 10)
        # 验证结果列表长度
        self.assertEqual(len(results), 10)
        # 验证每个操作都返回了一个值
        self.assertTrue(all(1 <= r <= 10 for r in results))


if __name__ == "__main__":
    unittest.main()
