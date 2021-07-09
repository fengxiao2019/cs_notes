"""
线程池技术
关键点：
    1. 线程怎么存储
    2. 怎么检查是否有空闲线程
    3. 任务存在哪里
    4. 怎么处理任务
"""
class ThreadPool(object):
    def __init__(self, max_workers=None, thread_prefix_name='', ):