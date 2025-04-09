def mean(data):
    """Calculate the mean (average) of the data."""
    return sum(data) / len(data)

def variance(data):
    """Calculate the variance of the data."""
    mean_val = mean(data)
    return sum((x - mean_val) ** 2 for x in data) / len(data)

def standard_deviation(data):
    """Calculate the standard deviation of the data."""
    return variance(data) ** 0.5

def median(data):
    """Calculate the median of the data."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        mid1, mid2 = sorted_data[n // 2 - 1], sorted_data[n // 2]
        return (mid1 + mid2) / 2


def pearson_correlation(x, y):
    """Calculate the Pearson correlation coefficient between two datasets."""

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
    denominator = (sum((x[i] - mean_x) ** 2 for i in range(len(x))) *
                   sum((y[i] - mean_y) ** 2 for i in range(len(y)))) ** 0.5

    return numerator / denominator


