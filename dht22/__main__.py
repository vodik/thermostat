import asyncio
import argparse
import contextlib

import aiozmq
import msgpack
import zmq

from .sensor import Sensor


async def dht22_poll(target, pin):
    sensor = Sensor(pin)
    subscription = sensor.subscribe()

    future = asyncio.ensure_future(sensor.poll())
    try:
        sender = await aiozmq.create_zmq_stream(zmq.PUSH, connect=target)
        with contextlib.closing(sender):
            while True:
                humidity, temperature = await subscription.read()
                sender.write((b'dht22', msgpack.packb({
                    'humidity': humidity,
                    'temperature': temperature
                })))
    finally:
        future.cancel()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='The target endpoint to send metrics')
    parser.add_argument('--pin', '-p', help='The GPIO pin to read')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(dht22_poll(args.target, args.pin))
    loop.close()


if __name__ == '__main__':
    main()
