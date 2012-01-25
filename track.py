import sys
import time
import datetime
import concurrent.futures

continue_ = True

def points(seconds=60):
    while continue_:
        time.sleep(seconds)
        print('.', end='')
        sys.stdout.flush()

def background(*args):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future   = executor.submit(*args)
    return future

if __name__=='__main__':
    background(points)
    for line in sys.stdin:
        print()
        print(datetime.datetime.now())
    continue_ = False
