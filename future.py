from functools import wraps


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


class Task:
    task_queue = []

    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_callback(self.step)

    @classmethod
    def coroutine(cls, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            cls.task_queue.append(fn)
            return Task(fn(*args, **kwargs))

        return wrapper
