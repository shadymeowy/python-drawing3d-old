import multiprocessing as mp


class ProxyInterface:
    def __init__(self, type, queue):
        self._cmd = []
        self.type = type
        self.queue = queue

    def commit(self):
        self.queue.put(self._cmd)
        self._cmd = []

    def __getattr__(self, name):
        if not hasattr(self.type, name):
            raise AttributeError(f'{self.type} has no attribute {name}')

        def wrapper(*args, **kwargs):
            self._cmd.append((name, args, kwargs))
        return wrapper

    def __call__(self, *args, **kwargs):
        self._cmd.append((None, args, kwargs))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()


class ProxyHandler:
    def __init__(self, queue, obj):
        self.queue = queue
        self._obj = obj

    def handle(self, skip_empty=False, discard=True):
        if skip_empty and self.queue.empty():
            return
        while True:
            cmd = self.queue.get()
            if self.queue.empty() or not discard:
                break
        for name, args, kwargs in cmd:
            getattr(self._obj, name)(*args, **kwargs)


class Proxy(ProxyInterface):
    def __init__(self, type, *args, **kwargs):
        self._queue = mp.Queue()
        super().__init__(type, self._queue)
        self._process = mp.Process(target=self._run, args=(self._queue, type, args, kwargs))
        self._process.start()

    def _run(self, queue, type, args, kwargs):
        obj = type(*args, **kwargs)
        handler = ProxyHandler(queue, obj)
        while True:
            handler.handle()

    def join(self):
        self._process.join()
