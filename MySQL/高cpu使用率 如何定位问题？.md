高cpu使用率 如何定位问题？

- 理解cpu时间花费在哪了？
- user space - 代码层级，eg ： mysql
- system  space - 系统切换
- iowait - 
- 等等。
mysql thread 活动监控
- Peak Threads Connected
- Peak Threads Running 
- Avg Threads Running
可以通过以下语句查看：
```Mysql
mysql> show status like 'thread%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_cached    | 7     |
| Threads_connected | 2     |
| Threads_created   | 10    |
| Threads_running   | 2     |
+-------------------+-------+
4 rows in set (0.01 sec)
```
检查线程数，确定是否是线程切换带来的cpu利用率飙升。

- 检查qps 
可以通过以下语句查看：
```Mysql
mysql> show status like 'ques%'\G;
*************************** 1. row ***************************
Variable_name: Questions
        Value: 54
1 row in set (0.09 sec)

ERROR: 
No query specified
```

- 查看instance 负载
mysql\> show status where variable_name in ('Com_select', 'Com_insert', 'Com_update', 'Com_delete')\G;
*************************** 1. row ***************************
Variable_name: Com_delete
Value: 2
*************************** 2. row ***************************
Variable_name: Com_insert
Value: 0
*************************** 3. row ***************************
Variable_name: Com_select
Value: 6
*************************** 4. row ***************************
Variable_name: Com_update
Value: 0
4 rows in set (0.00 sec)