# outliers.py

def z_score_outliers(data, threshold=3):
    """Identify outliers using the Z-score method."""
    mean_val = sum(data) / len(data)
    variance = sum((x - mean_val) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    outliers = [i for i, val in enumerate(data) if abs((val - mean_val) / std_dev) > threshold]
    return outliers


