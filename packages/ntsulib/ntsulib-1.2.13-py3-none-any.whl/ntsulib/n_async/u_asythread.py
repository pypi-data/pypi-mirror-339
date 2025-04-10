import asyncio
import inspect
from enum import Enum

class asythread_status(Enum):
    unstart:int = 0
    running:int = 1
    finish:int = 2

class n_asyerror(Exception):
    def __init__(self, message):
        self.message = message
        self.line_number = inspect.currentframe().f_back.f_lineno
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (line {self.line_number})"

# 协程线程池
class n_asyncThreadPool:
    def __init__(self, max_workers:int | None = None):
        self.max_workers = 5 if max_workers is None else max_workers
        self._status = asythread_status.unstart
        self._asythreads:list = []

    # 获取状态
    @property
    def getStatus(self) -> asythread_status:
        return self._status

    # 放入
    def put(self, func, *args, **kwargs):
        self._asythreads.append([func, args, kwargs])

    # 开始运行
    # 需要考虑maxworkers
    def start(self) -> list | None:
        if self._status == asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')
        self._status = asythread_status.running
        async def _in():
            # 创建所有协程任务
            tasks = []
            for item in self._asythreads:
                func = item[0]
                args = item[1]
                kwargs = item[2]
                tasks.append(func(*args, **kwargs))
            # 如果有最大并发数限制，使用信号量控制
            if self.max_workers is not None:
                semaphore = asyncio.Semaphore(self.max_workers)
                async def sem_task(task):
                    async with semaphore:
                        return await task
                # 使用信号量包装所有任务
                tasks = [sem_task(task) for task in tasks]
            # 并发执行所有任务
            return await asyncio.gather(*tasks, return_exceptions=True)
        try:
            result = asyncio.run(_in())
            self._status = asythread_status.finish
            return result
        except Exception as e:
            self._status = asythread_status.finish
            raise n_asyerror(f"Error during concurrent execution: {str(e)}")

    # 单个执行(只执行传入的)
    @classmethod
    def single_submit(cls, func, *args, **kwargs) -> any:
        async def _main():
            if args.__len__() == 0 and kwargs.__len__() == 0:
                coro = func()
            else:
                coro = func(*args, **kwargs)
            return await coro
        return asyncio.run(_main())

    def clear(self):
        if self._status == asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')
        self._asythreads.clear()
        self._status = asythread_status.unstart

    # 批量执行
    # 会返回结果
    # 参数必须传递位置参数
    def map(self, func, *args) -> list:
        if self._status == asythread_status.running:
            raise n_asyerror('Exist Task is Running, Start Failed')

        self._status = asythread_status.running

        async def _in():
            # 处理参数 - 将多个参数转换为参数元组
            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                # 处理 t.map(func, ((1,),(2,),(3,))) 的情况
                arg_sets = args[0]
            else:
                # 处理 t.map(func, 1, 2, 3) 或 t.map(func, (1,), (2,), (3,)) 的情况
                arg_sets = [(arg,) if not isinstance(arg, (list, tuple)) else arg for arg in args]

            # 创建所有协程任务
            tasks = []
            for arg_set in arg_sets:
                # 确保arg_set是可迭代的
                if not isinstance(arg_set, (list, tuple)):
                    arg_set = (arg_set,)
                tasks.append(func(*arg_set))

            # 如果有最大并发数限制，使用信号量控制
            if self.max_workers is not None:
                semaphore = asyncio.Semaphore(self.max_workers)

                async def sem_task(task):
                    async with semaphore:
                        return await task

                # 使用信号量包装所有任务
                tasks = [sem_task(task) for task in tasks]

            # 并发执行所有任务
            return await asyncio.gather(*tasks, return_exceptions=True)

        try:
            result = asyncio.run(_in())
            self._status = asythread_status.finish

            # 检查是否有异常结果
            for res in result:
                if isinstance(res, Exception):
                    raise n_asyerror(f"Task execution failed: {str(res)}")

            return result
        except Exception as e:
            self._status = asythread_status.finish
            raise n_asyerror(f"Error during map execution: {str(e)}")
