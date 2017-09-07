==============
DIY Thermostat
==============

My DIY thermostat project.

Still super alpha, very early in development, so don't expect to be able to run
anything. Don't stand by the code's quality yet.

I want to build myself a programmable thermostat while also being able to
distribute sensors around my apartment. This way I have the ability of
programming the thermostat based on the temperature recorded in different
rooms and different times of day. This will be particularity important as the
temperature between my living room and bedroom can vary by as much as 4
degrees.

Architecture
------------

Currently made of two parts:

Metric collection is handled by a standalone agent that pushes metrics into a
sensor network via zmq:

.. code ::

    python -m dht22 --pin 4 tcp://localhost:6667

Then a centralized daemon recieves incoming metrics, exposes the value over a
REST endpoint and a WebSocket, and also records the measurements into InfluxDB:

.. code ::

   python -m aiohttp.web thermostat.app:app_factory -H 0.0.0.0 -P 5000

What I want to move towards:

- Use zmq to stream sensor readings to a central broker.
- Expose recent readings over a WebSocket API and a REST API.
- Record measurements into InfluxDB.
- Expose another API for controlling the thermostat.
- Store all thermostat state change events in a persistent database for debugging.

Parts and Designs
-----------------

TODO

Notes
-----

- aioinflux is vendored from plugaai/aioinflux
- dht22 driver is based on the official Adafruit driver, but wrapped with Cython
