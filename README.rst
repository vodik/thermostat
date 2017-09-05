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

Currently there's a daemon that reads from a DHT22 sensor every two seconds,
exposes the value over a REST endpoint and a WebSocket, and also records the
measurements into InfluxDB.

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
