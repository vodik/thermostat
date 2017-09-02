import math


def dewpoint(t, rh):
    if t > 0:
        b, c = 17.368, 238.88
    else:
        b, c = 17.966, 247.15

    pa = rh / 100. * math.exp(b * t / (c + t))
    dp = c * math.log(pa) / (b - math.log(pa))
    return dp


def humidex(t, d):
    kelvin = 273.15
    temperature = t + kelvin
    dewpoint = d + kelvin

    # Calculate vapor pressure in mbar.
    e = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / dewpoint)))

    # Calculate saturation vapor pressure
    h = 0.5555 * (e - 10.0)

    humidex = temperature + h - kelvin
    return humidex


def humidex_level(humidex):
    if humidex >= 55:
        return 'Heat stroke probable'
    elif humidex >= 45:
        return 'Dangerous discomfort'
    elif humidex >= 40:
        return 'Intense discomfort; avoid exertion'
    elif humidex >= 35:
        return 'Evident discomfort'
    elif humidex >= 30:
        return 'Noticeable discomfort'
    else:
        return 'Little or no discomfort'
