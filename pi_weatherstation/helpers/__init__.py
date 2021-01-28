def evaluate_humidity(humidity):
    if humidity < 40:
        return "low"
    elif 40 <= humidity <= 60:
        return "good"
    else:
        return "high"


def evaluate_air_quality(air_quality):
    if air_quality is None:
        return "unavailable"
    if air_quality < 40:
        return "bad"
    else:
        return "good"
