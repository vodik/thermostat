import asyncio
import collections

from .rbp2 import *  # noqa


def read_mock():
    import random
    return random.uniform(30, 55), random.uniform(20, 34)


class Sensor:
    def __init__(self, pin, *, loop=None):
        self.pin = pin
        self.loop = loop or asyncio.get_event_loop()

        self._data = None
        self._waiters = collections.deque()
        self.counter = 0

    async def poll(self):
        self.future = self.loop.create_future()

        while True:
            if not self._waiters:
                self._data = None
                await asyncio.sleep(2)
                continue

            try:
                self._data = dht_read(self.pin)
                # self._data = read_mock()
            except RuntimeError:
                continue

            self.counter += 1
            for counter, fut in self._waiters:
                if not fut.done() and (counter is None or counter < self.counter):
                    fut.set_result((self.counter, self._data))

            await asyncio.sleep(2)

    def subscribe(self):
        return Subscribe(self)

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


class Subscribe:
    def __init__(self, sensor):
        self.sensor = sensor
        self.counter = 0

    async def read(self):
        while True:
            counter, data = await self.sensor.wait(counter=self.counter)
            if counter > self.counter:
                self.counter = counter
                return data
