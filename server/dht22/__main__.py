import asyncio
import argparse
import contextlib

import msgpack
import zmq
import zmq.asyncio

from .sensor import Sensor


context = zmq.asyncio.Context()


async def dht22_poll(target, pin, identifier):
    sensor = Sensor(pin)
    subscription = sensor.subscribe()
    identifier = f'dht22/{identifier}'.encode()

    future = asyncio.ensure_future(sensor.poll())
    try:
        sender = context.socket(zmq.PUSH)
        sender.connect('tcp://0.0.0.0:6667')
        with contextlib.closing(sender):
            while True:
                humidity, temperature = await subscription.read()
                print(f'Humiditiy={humidity:.2f}%, '
                      f'Temperature={temperature:.2f}')
                sender.send_multipart(
                    (identifier, msgpack.packb((humidity, temperature)))
                )
    finally:
        future.cancel()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='The target endpoint to send metrics')
    parser.add_argument('--pin', '-p', help='The GPIO pin to read')
    parser.add_argument('--id', '-i', help='An identifier')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(dht22_poll(args.target, args.pin, args.id))
    loop.close()


if __name__ == '__main__':
    main()
