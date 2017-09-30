from prometheus_client import Histogram, Gauge


REQ_TIME = Histogram(
    name="req_time_read_sensor",
    documentation="Time spent handling requests"
)

HUMIDITY = Gauge(
    name="sensor_humidity",
    documentation="Humidity read from a sensor",
    labelnames=['sensor', 'name']
)

TEMPERATURE = Gauge(
    name="sensor_temperature",
    documentation="Temperature read from a sensor",
    labelnames=['sensor', 'name']
)
