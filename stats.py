'''statistical analysis helper functions'''


def average(data): return sum(data)/len(data)


def median(data): return sorted(data)[len(data)//2]


def span(data): return max(data) - min(data)


def variance(data):
    mean = average(data)
    return sum((x-mean)**2 for x in data) / len(data)


def histogram(data):
    # vi i hate you
    pass
