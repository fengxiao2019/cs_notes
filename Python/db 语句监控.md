[db 语句监控][1]
```python
import logging
import time

logger = logging.getLogger(__name__)
THRESHOLD_SECONDS = 1.0


def slow_query_warner(execute, sql, params, many, context):
    start = time.perf_counter()
    result = execute(sql, params, many, context)
    duration = time.perf_counter() - start
    if duration > THRESHOLD_SECONDS:
        logger.warning("Slow query, took %.2f seconds: %s", duration, sql)
    return result

# from django.db import connection

with connection.execute_wrapper(warn_about_slow_queries):
    res = Video.objects.filter(title__startswith='sj')
    for item in res:
        print(res.title)
```

可以通过以middleware的形式监控所求的request请求中的慢查询
```python
from django.db import connection


class SlowQueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with connection.execute_wrapper(slow_query_warner):
            return self.get_response(request)
```

middleware 的形式虽然能够监控所有通过http 请求触发的db 操作，但是，对于一些常驻进程或者一些脚本中的查询无法覆盖到，还有一种方式可以实现全局监控，那就是利用`connection_created` 信号将相关检查函数放到`executed_wrappers`中，但是该函数没有在文档中体现出来，所以要写一下上线前测试的用例，以防版本升级无法使用。
实现方式：
```python
from django.db import connections
from django.db.backends.signals import connection_created


def install_slow_query_warner(connection, **kwargs):
    """
    Install slow_query_warner on the given database connection.
    Rather than use the documented API of the `execute_wrapper()` context
    manager, directly insert the hook.
    """
    if slow_query_warner not in connection.execute_wrappers:
        connection.execute_wrappers.append(slow_query_warner)


connection_created.connect(install_slow_query_warner)
for connection in connections.all():
    install_slow_query_warner(connection=connection)
```
这段代码可以放到任意一个app的AppConfig.ready()方法中。

测试用例：
```python
from unittest import mock

from django.db import connection
from django.test import TestCase

import __main__


class SlowQueryWarnerTests(TestCase):
    @mock.patch.object(__main__, 'THRESHOLD_SECONDS', 0.01)
    def test_slow_query(self):
        with self.assertLogs('__main__') as logged, connection.cursor() as cursor:
            cursor.execute("SELECT SLEEP(0.02)")

        self.assertEqual(len(logged.records), 1)
        self.assertTrue(logged.records[0].msg.startswith("Slow query, took "))
```

[1]:	https://adamj.eu/tech/2020/07/23/how-to-make-always-installed-django-database-instrumentation/ "慢查询监控"