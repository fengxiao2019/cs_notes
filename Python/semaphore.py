import logging
import threading
import time
import random
import os


LOG_FORMAT = f"%(asctime)s %(threadName) 17s %(levelname) -8s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

semaphore = threading.Semaphore(0)
lock = threading.Lock()
cond = threading.Condition()
event = threading.Event()
item = 0
items = []
# 用event实现生产者 消费者

def consume():
    while True:
        event.wait()
        logging.info("wait;w")
        if items:
            item = items.pop()
            logging.info(f'get it {item} -pid: {os.getpid()}')
        time.sleep(1)

def produce():
    while True:
        for i in range(5):
            items.append(random.randint(0, 10000))
            logging.info(f'-----produce item: {items} -pid: {os.getpid()}')
        event.set()
        time.sleep(1)
        event.clear()


def main():

    t2 = threading.Thread(target=produce)
    t2.start()
    t2.join()
    threads = [threading.Thread(target=consume) for i in range(7)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


if __name__ == '__main__':
    main()