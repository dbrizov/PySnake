def clamp(value, min, max):
    if (value < min):
        value = min
    elif (value > max):
        value = max

    return value
