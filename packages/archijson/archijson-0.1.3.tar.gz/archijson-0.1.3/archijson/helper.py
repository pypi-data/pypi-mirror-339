
def identity(n):
    arr = [0. for i in range(n * n)]
    for i in range(n):
        arr[i * n + i] = 1.
    return arr


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


