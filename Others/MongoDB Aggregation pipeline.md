## 什么是Aggregation Pipeline
它利用阶段来过滤数据并执行分组、排序和转换每个操作者的输出等操作。这个框架是MongoDB的MapReduce功能的替代方案，输出可以被输送到一个新的集合，或用于更新特定的文档。
![][image-1]
## Aggregation pipeline vs mapreduce
1. 聚合管道运行的是编译的C++代码，MapReduce的Javascript代码是解释的。
2. 聚合管道的不再需要对BSON MongoDB文档进行转换，变成JSON进行读取，因为它没有使用Javascript。MapReduce操作会更慢，因为它必须将BSON支持的双数、32位整数和64位整数转换为Javascript的所有数字的一个整数类型。如果查询中包括对数据库的写入，这也会进一步延迟，因为数字必须再次转换。

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNgy1grnltkwc9mj30pu03et98.jpg