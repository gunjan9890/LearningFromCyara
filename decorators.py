import math
import random


def retry_test(num_times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num_times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Retrying {func.__name__} for the {i+1} time")
            return None
        return wrapper
    return decorator


@retry_test(num_times=3)
def simple_test():
    print("Simple Test")
    i = random.Random().randint(0, 9)
    if i < 8 :
        assert False

simple_test()
