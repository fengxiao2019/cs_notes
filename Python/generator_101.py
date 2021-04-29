from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(max_workers=10)

def run():
    fut = pool.submit(func, 2, 3)
    fut.add_done_callback(result_handler)

def result_handler(fut):
    # 异常的处理在callback里面
    try:
        result = fut.result()
        print('Got:', result)
    except Exception as e:
        print('Failed: %s: %s' % (type(e).__name__, e))



