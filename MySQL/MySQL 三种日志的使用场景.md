## binlog
二进制日志，属于server层的日志
使用场景：
1. master - slave 数据同步
2. 外部数据同步（利用cannal 同步到ES、消息队列等）
3. 数据恢复，系统宕机，可以利用binglog恢复数据
## redolog
物理日志，属于引擎层的日志
使用场景：
事务数据恢复
## undolog
数据日志，属于引擎层