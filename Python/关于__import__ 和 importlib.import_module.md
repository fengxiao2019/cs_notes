关于__import__ 和 importlib.import_module

文件目录结构如下：
```python
daily
   -- 20210504
      permutations.py
      __init__.py
   __init__.py
```
我想import permutations 这个module，一般情况下，我们的写法是：
```python
import daily.20210504.permutations
```
但是因为中间有个module的name是数字，这种写法是行不通的，怎么实现呢？
可以通过__import__ 或者 importlib.import_module实现。
官方文档推荐使用importlib.import_module。
> __import__(name, globals=None, locals=None, fromlist=(), level=0) -> module
>  Import a module. Because this function is meant for use by the Python interpreter and not for general use, it is better to useimportlib.import_module()to programmatically import a module.
区别是什么呢？
如果使用__import__实现的话：
例如：
```python
res = __import__('daily.20210504.permutations')
```
res的结果是daily 模块：
![][image-1]
所以，如果想要获得`permutations`模块，需要提供fromlist参数，具体写法如下：
```python
res = __import__('daily.20210504.permutations', fromlist=('daily.20210504'))
```
res的结果可以看到现在是：
![][image-2]
现在是我们要想要的结果了。

如果使用importlib.import_module呢？
```python
res = importlib.import_module('daily.20210504.permutations')
```
这样就可以直接获取permutations模块。

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1gq693k7dt0j31fq01qjrt.jpg
[image-2]:	https://tva1.sinaimg.cn/large/008i3skNly1gq697050zxj31tw01ggls.jpg