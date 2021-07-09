## 查询层面的优化：
- 使用索引，不要在主键中使用多个列，因为这些列的值会在每个二级索引中重复出现。当一个索引包含不必要的数据时，读取这些数据的I/O和缓存这些数据的内存会降低服务器的性能和扩展性。
- 尽量使用组合索引，不要为每个列都创建索引，如果你对同一张表有许多查询，测试不同的列组合，试着创建少量的联合索引而不是大量的单列索引。如果一个索引包含了结果集所需的所有列（称为覆盖索引），那么查询可能完全可以避免读取表的数据。
- 如果一个索引列不能包含任何NULL值，那么在创建表的时候将其声明为NOT NULL。当优化器知道每个列是否包含NULL值时，它可以更好地确定哪一个索引对查询最有效。
- 最左前缀匹配
- 数据类型和数据类型保持一致
- 避免使用%开头的模糊查询
- 不要在区分度不高的字段上添加索引
- 不要在频繁更新的字段上添加索引
- 在明确字段大小的情况下使用小字段
- 
## 索引添加的规则
三星索引

## 慢查询问题定位
Identify the query (either manually or with a tool like PMM)
Check the EXPLAIN plan of the query
Review the table definition
Create indexes
-Start with columns in the WHERE clause
-For composite indexes, start with the most selective column and work to the least selective column
-Ensure sorted columns are at the end of the composite index
Review the updated explain plan and revise as needed
Continue to review the server to identify changes in access patterns that require new indexing
借助工具：pt-query-digest
引用：
[https://www.percona.com/blog/2020/06/26/mysql-101-how-to-find-and-tune-a-slow-sql-query/][1]
[https://www.percona.com/doc/percona-toolkit/2.2/pt-query-digest.html][2]

[1]:	https://www.percona.com/blog/2020/06/26/mysql-101-how-to-find-and-tune-a-slow-sql-query/
[2]:	https://www.percona.com/doc/percona-toolkit/2.2/pt-query-digest.html