def evaluate_humidity(humidity):
    if humidity < 40:
        return "low"
    elif 40 <= humidity <= 60:
        return "good"
    else:
        return "high"
