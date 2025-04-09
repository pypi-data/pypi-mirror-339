"""
测试 async-sync 集成场景
Test async-sync integration scenarios
"""

import asyncio
import time
import unittest

import async_sync


class TestIntegration(unittest.TestCase):
    def test_complex_workflow(self):
        """测试复杂工作流中混合使用同步和异步函数"""

        def sync_task(value):
            time.sleep(0.1)
            return value * 2

        async def async_task(value):
            await asyncio.sleep(0.1)
            return value + 10

        # 将同步函数转为异步
        async_sync_task = async_sync.to_async(sync_task)

        # 将异步函数转为同步
        _ = async_sync.to_sync(async_task)

        # 创建混合工作流
        async def workflow():
            # 同时运行多个异步任务
            tasks = [async_task(i) for i in range(3)] + [
                async_sync_task(i) for i in range(3, 6)
            ]

            results = await asyncio.gather(*tasks)
            return results

        # 在同步代码中执行工作流
        workflow_results = async_sync.run_async_in_sync(workflow())

        # 验证结果
        expected = [10, 11, 12, 6, 8, 10]
        self.assertEqual(workflow_results, expected)

    def test_exception_handling(self):
        """测试异常处理情况"""

        async def async_raises():
            await asyncio.sleep(0.1)
            raise ValueError("Async exception")

        def sync_raises():
            time.sleep(0.1)
            raise RuntimeError("Sync exception")

        # 测试同步调用异步出现异常
        with self.assertRaises(ValueError):
            async_sync.run_async_in_sync(async_raises())

        # 测试异步调用同步出现异常
        async def test_sync_exception():
            with self.assertRaises(RuntimeError):
                await async_sync.run_sync_in_async(sync_raises)

        asyncio.run(test_sync_exception())

    def test_concurrent_execution(self):
        """测试并发执行场景"""

        def slow_sync_function(delay, value):
            time.sleep(delay)
            return value

        async def test_concurrent():
            # 使用线程池并发执行多个同步函数
            start_time = time.time()

            tasks = [
                async_sync.run_sync_in_async(slow_sync_function, 0.5, i)
                for i in range(5)
            ]

            results = await asyncio.gather(*tasks)

            end_time = time.time()
            duration = end_time - start_time

            # 验证结果正确
            self.assertEqual(results, list(range(5)))

            # 验证总执行时间小于所有任务串行执行的时间
            # 如果串行执行需要约 2.5 秒，并发应该明显更快
            self.assertLess(duration, 1.5)

        asyncio.run(test_concurrent())


if __name__ == "__main__":
    unittest.main()
