import async_sync
import asyncio
import time


# 示例1: 使用装饰器将异步函数转换为同步函数
@async_sync.to_sync
async def fetch_data():
    """模拟异步数据获取操作"""
    await asyncio.sleep(1)
    return "数据已获取"


# 在同步代码中直接调用
result = fetch_data()
print(f"同步调用结果: {result}")


# 示例2: 在异步环境中也可以使用转换后的函数
async def async_example():
    result = fetch_data()  # 不需要await
    print(f"异步环境中调用结果: {result}")


asyncio.run(async_example())


# 示例3: 使用run_async_in_sync直接运行协程
async def process_data():
    await asyncio.sleep(0.5)
    return "处理完成"


print(f"直接运行协程: {async_sync.run_async_in_sync(process_data())}")


# 示例4: 将同步函数转换为异步函数
def cpu_intensive_task(duration):
    """模拟CPU密集型任务"""
    time.sleep(duration)
    return f"任务完成，耗时{duration}秒"


# 转换为异步函数
async_task = async_sync.to_async(cpu_intensive_task)

print(f"CPU密集型任务异步调用: {asyncio.run(async_task(1.5))}")
print("所有示例运行完毕!")
