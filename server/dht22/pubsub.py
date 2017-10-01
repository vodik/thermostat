import asyncio
import collections


class Publisher:
    def __init__(self, *, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.counter = 0
        self._data = None
        self._waiters = collections.deque()

    def publish(self, data):
        self._data, self.counter = data, self.counter + 1

        for counter, fut in self._waiters:
            if not fut.done() and (counter is None or counter < self.counter):
                fut.set_result((self.counter, self._data))

    def subscribe(self):
        return Subscriber(self)

    @property
    def empty(self):
        return not bool(self._waiters)

    async def wait(self, *, counter=None):
        if self._data and counter is not None and self.counter > counter:
            return self.counter, self._data

        fut = self.loop.create_future()
        entry = counter, fut
        self._waiters.append(entry)
        try:
            return await fut
        finally:
            self._waiters.remove(entry)

    async def read(self):
        if self._data:
            return self._data

        fut = self.loop.create_future()
        entry = 0, fut
        self._waiters.append(entry)
        try:
            _, data = await fut
            return data
        finally:
            self._waiters.remove(entry)


class Subscriber:
    def __init__(self, sensor):
        self.sensor = sensor
        self.counter = 0

    async def read(self):
        while True:
            counter, data = await self.sensor.wait(counter=self.counter)
            if counter > self.counter:
                self.counter = counter
                return data
