import asyncio
import collections

from aioinflux import AsyncInfluxDBClient

from .rbp2 import dht_read
from .pubsub import Publisher


def read_mock():
    import random
    return random.uniform(30, 55), random.uniform(20, 34)


class Sensor:
    def __init__(self, pin, *, loop=None):
        self.pin = pin
        self.publisher = Publisher()

    async def poll(self):
        while True:
            try:
                # data = dht_read(self.pin)
                data = read_mock()
            except RuntimeError:
                continue

            self.publisher.publish(data)
            await asyncio.sleep(2)

    def subscribe(self):
        return self.publisher.subscribe()
