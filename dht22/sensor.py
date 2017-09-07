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
        self.loop = loop or asyncio.get_event_loop()

        self.client = AsyncInfluxDBClient(database='sensors')
        self.publisher = Publisher()

    async def poll(self):
        while True:
            try:
                data = dht_read(self.pin)
                # data = read_mock()
            except RuntimeError:
                continue

            self.publisher.publish(data)

            asyncio.ensure_future(self.client.write({
                'measurement': 'dht22',
                'tags': {'sensor': 'dht22',
                         'location': 'office'},
                'fields': {'temperature': self._data[0],
                           'humidity': self._data[1]}
            }))
            await asyncio.sleep(2)

    def subscribe(self):
        return self.publisher.subscribe()
