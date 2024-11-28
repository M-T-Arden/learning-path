"""
异步操作的主要作用是提高程序的效率和响应性，
尤其是在处理I/O密集型任务（如网络请求、文件读写等）时。
通过异步操作，程序可以在等待某些操作（如网络响应）完成的同时，
继续执行其他任务，从而充分利用系统资源。

事件循环（event loop）是异步编程的核心机制。
它是一个运行在一个单独线程中的循环，负责调度和执行异步任务和回调。
事件循环会跟踪哪些任务已经准备好执行，哪些任务需要等待某些事件的发生（如I/O操作完成），
并在适当的时候调用相应的回调函数。
"""
#用上下文管理器的方式写asyncio.run()
#async with 用于管理异步上下文，例如文件操作、网络连接等，
# 通常需要在类中定义 __aenter__ 和 __aexit__ 方法。
#asyncio.run() 返回一个结果，通常是协程的返回值。不接受上下文管理器。
import asyncio

async def main():
    await asyncio.sleep(0.5) #这行代码让异步函数暂停2秒，模拟异步操作
    #这意味着在 say_hi 函数等待的这段时间里，事件循环可以运行其他任务。
    #print('Hello World!')
#with asyncio.Runner() as runner:
    #runner.run(main()) #get_loop()返回关联到运行器实例的事件循环。

# 获取当前上下文中的事件循环。如果当前上下文没有事件循环，它会创建一个新的事件循环。
# 运行直到异步函数被完成。
#asyncio.get_event_loop().run_until_complete(main())

"""
迭代器 (Iterator):
迭代器是一个对象，它实现了 next() 方法，
该方法会返回一个包含两个属性的对象：value 和 done。
value 表示当前迭代到的值。
done 是一个布尔值，表示迭代是否完成（true 表示完成，false 表示未完成）。
异步迭代器 (Async Iterator):
异步迭代器是迭代器的异步版本。
异步迭代器对象的 anext() 方法返回一个awaitable对象，
该对象解析为 value是迭代的当前值和 done 是布尔值。
"""

#异步迭代器不需要 async with，只需要定义 __aiter__ 和 __anext__ 方法。
class asyncfibo:
    def __init__(self, max_value):
        self.max_value = max_value
        self.previous =0
        self.current = 1
    def __aiter__(self):
        return self
    async def __anext__(self):
        if self.current <= self.max_value:
            await asyncio.sleep(self.previous)
            value = self.current
            self.previous, self.current= self.current, self.previous+self.current
            return value
        else:
            raise StopAsyncIteration
#使用 async for 迭代异步迭代器。
async def main():
    async for value in asyncfibo(5):
        print(value)
#asyncio.run(main())

#使用异步生成器实现更多资源的分配
class AsyncGenerator:
    def __init__(self, name):
        self.file_name = name
    async def __aenter__(self):
        #异步进入上下文，打开文件等资源
        self.op_file = open(self.file_name, 'w')
        print(f'file: {self.file_name} opened')
        return self #返回对象供上下文使用
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        #异步退出上下文
        if self.op_file is not None:
            self.op_file.close()
            print(f'file: {self.file_name} closed')
        else:
            print(exc_type, exc_val, exc_tb)
        return False #异常未处理则抛出
    async def write_data(self,data):
        #这里怎么不加上self.obj.seek(0)
        await asyncio.sleep(1)
        self.op_file.write(data)
        self.op_file.flush()  # 确保数据立即写入磁盘
        print(f'file: {self.file_name} written {data}')
    async def read_data(self):
        # 重新打开文件并读取内容
        with open(self.file_name, 'r') as file:
            await asyncio.sleep(1)  # 模拟异步操作
            data = file.read()
            print(f'File: {self.file_name} read: {data}')
            return data

async def main():
    # 使用异步资源管理器
    async with AsyncGenerator('example.txt') as manager:
        await manager.write_data("Hello, Async World!\n")
        await manager.write_data("Managing multiple resources is easy.\n")
        content = await manager.read_data()
        print(f"Content:\n{content}")
# 执行主函数
asyncio.run(main())





