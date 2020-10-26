from queue import Queue
from threading import Thread, get_ident
import time
from memory_profiler import profile

q = Queue()
print(dir(q))
[q.put(i) for i in range(4)]

@profile
def do_work(item):
    dicts = [{} for _ in range(1000)]
    print(f'Thread id is {get_ident()}')
    print(f'test item: {item}')
    # return dicts


def worker():
    while not q.empty():
        item = q.get()
        try:
            time.sleep(1)
            do_work(item)
        finally:
            q.task_done()


@profile
def thread():
    threads = [Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    worker()
    q.join()
    print('End')


if __name__ == '__main__':
    thread()