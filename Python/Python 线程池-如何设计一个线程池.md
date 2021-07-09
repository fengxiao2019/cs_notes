Python 线程池-如何设计一个线程池
## ThreadPoolExecutor源码解读
适用于CPU bound task which releases GIL
```python
def __init__(self, max_workers=None, thread_name_prefix='',
                 initializer=None, initargs=()):
```
其中，`max_workers`是最大线程数，默认是cpu的核数 + 4
```python
if max_workers is None:
            # ThreadPoolExecutor is often used to:
            # * CPU bound task which releases GIL
            # * I/O bound task (which releases GIL, of course)
            #
            # We use cpu_count + 4 for both types of tasks.
            # But we limit it to 32 to avoid consuming surprisingly large resource
            # on many core machine.
            max_workers = min(32, (os.cpu_count() or 1) + 4)
```
**如何得知当前线程池里面是否有空闲线程？如何避免空闲线程竞争？**
在初始化中，定义了一个信号量
```python
self._idle_semaphore = threading.Semaphore(0)
```
线程池实现的方式类似懒加载的方式，当有新的任务需要被处理时，先检查是否有空闲的线程（通过信号量），如果不存在，就创建新的线程处理任务。
**信号量的值被初始化为0，怎么实现是否有空闲线程的？**
每次处理完任务后，会调用信号量的释放操作，信号量的释放操作，对应的`_value`会加1，这样就能实现空闲线程数和信号量的`_value`一致。
```python

        while True:
            work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run()
                # Delete references to object. See issue16284
                del work_item

                # attempt to increment idle count
                executor = executor_reference()
                if executor is not None:
                    executor._idle_semaphore.release()
                del executor
                continue
```
**线程池中的线程存在哪里的？**
```python
self._threads = set()
```
**线程池待处理的任务是存在哪的？如何避免竞争的？**
通过queue存储，并且通过queue避免竞争
```python
self._work_queue = queue.SimpleQueue()
```
**线程的名字？**
```python
self._thread_name_prefix = (thread_name_prefix or
                                    ("ThreadPoolExecutor-%d" % self._counter()))

num_threads = len(self._threads) # set()
thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                     num_threads)
```

**任务怎么添加到任务队列（`self._work_queue `）中的？**
通过submit函数
```python
def submit(*args, **kwargs):
```
参数一般是执行函数和执行函数所需要的参数
返回值是一个Future对象
例如：
```python
future = pool.submit(step_cell, *args)
```
**future 存储到了哪里？**
future 对象被装进WorkItem，扔进了`self._queue`中，等待线程从`self._queue`中拿出来进行处理。
## Future 对象
## 如何设计一个线程池？


