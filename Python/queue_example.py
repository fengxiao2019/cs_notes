"""
任务
要构建这样一个系统
1. 持续从数码相册中获取照片
1. 调整照片的尺寸
2. 放回到相册中
思想：创建三个队列
一个或者一组线程处理一个队列
第一个队列负责下载照片， 并放到第二个队列中
第二个队列负责调整尺寸，并放到第三个队列中
第三个队列负责上传照片
"""
# 阻塞队列
from queue import Queue
from threading import Thread
# 下载照片
def download(item):
    print(f"downloaded {item}")
    return item

# 调整照片的尺寸
def resize(item):
    print(f"resized {item}")
    return item

# 放回到相册中
def upload(item):
    print(f"upload {item}")
    return item


class ClosableQueue(Queue):
    SENTINEL = object()  # 表示队列任务结束的标志 哨兵对象

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super(StoppableWorker, self).__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)


"""
组装
"""

def compose():
    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    upload_queue = ClosableQueue()
    done_queue = ClosableQueue()
    threads = [
        StoppableWorker(download, download_queue, resize_queue),
        StoppableWorker(resize, resize_queue, upload_queue),
        StoppableWorker(upload, upload_queue, done_queue)
    ]
    for _ in range(1000):
        download_queue.put(object())
    download_queue.close()

    for thread in threads:
        thread.start()
    # 等待下载的数据全部处理完
    download_queue.join()
    resize_queue.close() # 关闭resize 队列
    resize_queue.join()
    upload_queue.close() # 关闭上传队列
    upload_queue.join()
    print(done_queue.qsize(), "items finished")
    for thread in threads:
        thread.join()


"""
怎么扩展
一组线程处理下载任务
一组线程处理resize任务
一组线程处理上传任务
"""
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads


def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()

    closable_queue.join()
    for thread in threads:
        thread.join()

"""
queue模块提供了多个队列实现
LIFO 队列
优先队列 queue + heapq
simpleQueue
"""