import threading
import time
from enum import Enum
from queue import Queue, Empty
from typing import Callable, Any, List, Iterator, Union

__all__ = ["ThreadPoolStatus", "n_ThreadPool"]

class ThreadPoolStatus(Enum):
    unstarted = 0
    running = 1
    finished = 2
    terminated = 3


class n_ThreadPool:
    def __init__(self, max_workers: int = 5, daemon: bool = False):
        self.max_workers = max_workers
        self.daemon = daemon
        self.status = ThreadPoolStatus.unstarted
        self.task_count = 0
        self.task_finished_count = 0
        self.task_unfinished_count = 0

        self._task_queue = Queue()
        self._result_queue = Queue()
        self._workers = []
        self._stop_event = threading.Event()

        # 分组控制参数
        self._group_size = 0
        self._group_interval = 0.0

        # 同步锁
        self._lock = threading.Lock()

    def setGroupExecInterval(self, group: int, time_interval: float):
        if group < 0:
            raise ValueError("Group size cannot be negative")
        if time_interval < 0:
            raise ValueError("Time interval cannot be negative")
        self._group_size = group
        self._group_interval = time_interval

    def put(self, func: Callable, *args, **kwargs):
        if self.status in (ThreadPoolStatus.running, ThreadPoolStatus.finished):
            raise RuntimeError("Cannot add tasks after pool has started")

        with self._lock:
            self._task_queue.put((func, args, kwargs))
            self.task_count += 1
            self.task_unfinished_count += 1

    def start(self) -> None:
        if self.status != ThreadPoolStatus.unstarted:
            raise RuntimeError("Pool can only be started from unstarted state")

        self.status = ThreadPoolStatus.running
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.daemon = self.daemon
            worker.start()
            self._workers.append(worker)

    def startAndWait(self) -> List[Any]:
        self.start()
        return list(self._result_generator())

    def map(self, func: Callable, *iterables, timeout: Union[float, None] = None) -> Iterator:
        """类似ThreadPoolExecutor.map的行为，返回迭代器"""
        if self.status != ThreadPoolStatus.unstarted:
            raise RuntimeError("Pool can only be started from unstarted state")

        arg_sets = self._prepare_args(*iterables)
        for arg_set in arg_sets:
            self.put(func, *arg_set)

        self.start()
        return self._result_generator(timeout)

    def _result_generator(self, timeout: Union[float, None] = None) -> Iterator:
        """结果生成器，带超时控制"""
        remaining = self.task_count
        start_time = time.time()

        while remaining > 0:
            try:
                # 计算剩余超时时间
                remaining_time = None
                if timeout is not None:
                    elapsed = time.time() - start_time
                    remaining_time = max(0, timeout - elapsed)

                result = self._result_queue.get(timeout=remaining_time)
                remaining -= 1
                yield result
            except Empty:
                # 超时后强制终止线程池
                self.stopAnyWay()
                raise RuntimeError("ThreadPool operation timed out")
            except Exception as e:
                self.stopAnyWay()
                raise RuntimeError(f"ThreadPool error: {str(e)}")

    def clear(self):
        if self.status == ThreadPoolStatus.running:
            raise RuntimeError("Cannot clear tasks while pool is running")

        with self._lock:
            while not self._task_queue.empty():
                self._task_queue.get()
            self.task_count = 0
            self.task_unfinished_count = 0
            self.task_finished_count = 0
            self.status = ThreadPoolStatus.unstarted

    def stopAnyWay(self):
        """更可靠的终止方法"""
        self.status = ThreadPoolStatus.terminated
        self._stop_event.set()

        # 清空所有队列
        with self._lock:
            while not self._task_queue.empty():
                self._task_queue.get()
            while not self._result_queue.empty():
                self._result_queue.get()

        # 终止工作线程
        for worker in self._workers:
            if worker.is_alive():
                worker.join(timeout=0.1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.stopAnyWay()
        elif self.status == ThreadPoolStatus.running:
            # with块结束时自动等待完成
            list(self._result_generator())  # 消费所有结果
        return False

    def _worker(self):
        while not self._stop_event.is_set():
            try:
                if self._group_size > 0:
                    tasks = []
                    for _ in range(self._group_size):
                        if not self._task_queue.empty():
                            tasks.append(self._task_queue.get_nowait())

                    if tasks:
                        for task in tasks:
                            self._process_task(task)

                        if not self._task_queue.empty() and self._group_interval > 0:
                            time.sleep(self._group_interval)
                else:
                    task = self._task_queue.get(timeout=0.1)
                    self._process_task(task)
            except Exception:
                continue

            # 检查任务完成情况
            with self._lock:
                if self.task_finished_count == self.task_count:
                    self.status = ThreadPoolStatus.finished
                    break

    def _process_task(self, task):
        func, args, kwargs = task
        try:
            result = func(*args, **kwargs)
            self._result_queue.put(result)
        except Exception as e:
            self._result_queue.put(e)
        finally:
            with self._lock:
                self.task_finished_count += 1
                self.task_unfinished_count -= 1

    def _prepare_args(self, *iterables):
        """准备参数，支持标准库map风格的参数"""
        if not iterables:
            return []

        # 单个可迭代参数
        if len(iterables) == 1:
            iterable = iterables[0]
            if isinstance(iterable, (list, tuple)):
                return [(item,) for item in iterable]
            return [(item,) for item in iterable]

        # 多个可迭代参数
        return list(zip(*iterables))