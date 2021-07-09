发生这种情况的一种情况是，优化器估计使用索引将要求MySQL访问表中很大比例的行。在这种情况下，表扫描可能会快得多，因为它需要较少的搜索）。然而，如果这样的查询使用LIMIT只检索一些行，MySQL还是会使用索引，因为它可以更快找到结果中要返回的几条行。
- 类型不匹配：最常见是是字符串和数字
数据库的字段是字符串类型，查询的时候用数字。数据库为什么不把数字转成字符串呢？因为一个数字可以有多个字符串代表，例如5这个数字，“5” “005” “05”都能表示数字5。
但是，如果你的数据库中存储的字段类型是数字，你用字符串去查询是可以使用索引的，因为字符串表示的数字只有一种结果。
[https://www.percona.com/blog/2006/09/08/why-index-could-refuse-to-work/][1]
- 使用!= 或者 \<\> 导致索引失效
- 函数导致的索引失效
```sql
SELECT * FROM user` WHERE DATE(create_time) = '2020-09-03';
```
- 运算符导致的索引失效
```sql
SELECT * FROM user` WHERE age - 1 = 20;
```
如果你对列进行了（+，-，*，/，!）, 那么都将不会走索引。*
- NOT IN、NOT EXISTS导致索引失效
- 模糊搜索导致的索引失效
```sql
`SELECT * FROM user WHERE name` LIKE '%冰';
```
引用：
[https://dev.mysql.com/doc/refman/5.6/en/index-btree-hash.html#hash-index-characteristics][2]
[https://segmentfault.com/a/1190000023911554][3]

[1]:	https://www.percona.com/blog/2006/09/08/why-index-could-refuse-to-work/
[2]:	https://dev.mysql.com/doc/refman/5.6/en/index-btree-hash.html#hash-index-characteristics
[3]:	https://segmentfault.com/a/1190000023911554