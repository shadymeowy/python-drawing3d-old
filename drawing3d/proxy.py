import multiprocessing as mp


class ProxyInterface:
    def __init__(self, type, conn):
        self._cmd = []
        self.type = type
        self.conn = conn

    def commit(self):
        self.conn.send(self._cmd)
        self._cmd = []

    def __getattr__(self, name):
        if not hasattr(self.type, name):
            raise AttributeError(f'{self.type} has no attribute {name}')

        def wrapper(*args, **kwargs):
            self._cmd.append((name, args, kwargs))
        return wrapper

    def __call__(self, *args, **kwargs):
        self._cmd.append((None, args, kwargs))

    def stop(self):
        self.conn.send(None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()


class ProxyHandler:
    def __init__(self, conn, obj):
        self.conn = conn
        self._obj = obj

    def handle(self, discard=False):
        if not self.conn.poll():
            return True
        while True:
            cmd = self.conn.recv()
            if cmd is None:
                return False
            if not self.conn.poll() or not discard:
                break
        for name, args, kwargs in cmd:
            getattr(self._obj, name)(*args, **kwargs)
        return True


class Proxy(ProxyInterface):
    def __init__(self, type, *args, **kwargs):
        self._conn1, self._conn2 = mp.Pipe(duplex=False)
        super().__init__(type, self._conn2)
        self._process = mp.Process(target=self._run, args=(self._conn1, type, args, kwargs))
        self._process.start()

    def _run(self, conn, type, args, kwargs):
        obj = type(*args, **kwargs)
        handler = ProxyHandler(conn, obj)
        while handler.handle():
            pass

    def join(self):
        self._process.join()
