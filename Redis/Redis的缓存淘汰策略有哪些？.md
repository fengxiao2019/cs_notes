建议缓存容量设置成总数据量的%15～%30.
![][image-1]
volatile-ttl 在筛选时，会针对设置了过期时间的键值对，根据过期时间的先后进行删除，越早过期的越先被删除。
volatile-random 就像它的名称一样，在设置了过期时间的键值对中，进行随机删除。
volatile-lru 会使用 LRU 算法筛选设置了过期时间的键值对。
volatile-lfu 会使用 LFU 算法选择设置了过期时间的键值对。

allkeys-random 策略，从所有键值对中随机选择并删除数据；
allkeys-lru 策略，使用 LRU 算法在所有数据中进行筛选。
allkeys-lfu 策略，使用 LFU 算法在所有数据中进行筛选。

相关的配置：
```sql
CONFIG SET maxmemory 4gb
```

LRU的实现原理

LFU的实现原理

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1gs6vj0gpiqj61ct0l9wh802.jpg