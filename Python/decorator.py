# 实现一个处理耗时的decorator
from functools import wraps
from time import time, sleep


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        duration = int(time() - start)
        print(f"{func.__name__} took {duration} seconds")
        return res
    return wrapper


@timer
def f():
    sleep(1)