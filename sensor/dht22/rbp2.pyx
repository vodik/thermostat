cdef int DHT22 = 22


cdef import from "pi_2_dht_read.h":
    int pi_2_dht_read(int type, int pin, float* humidity, float* temperature)


def dht_read(pin):
    cdef float humidity, temperature
    if pi_2_dht_read(DHT22, pin, &humidity, &temperature) < 0:
        raise RuntimeError("Failed to read pin")

    return humidity, temperature
