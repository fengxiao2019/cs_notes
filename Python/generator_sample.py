# coding=utf8

# Iteration
for x in [1, 4, 5, 10, 12]:
    print(x)

# Iterating over a dict
prices = {'GOOG': 490.10,
          'AAPL': 145.23,
          'YHOO': 21.71}
for key in prices:
    print(key)

for k in prices.iterkeys():
    print(k)

for k, v in prices.items():
    print(k, v)

for k in prices.items():
    print(k)

# define a object to support iteration
# 实现一个支持iteration的对象，只需要实现__iter__和next这两个方法即可。


class countdown(object):
    def __init__(self, start):
        self.count = start

    def __iter__(self):
        return self

    def next(self):
        if self.count <= 0:
            raise StopIteration
        else:
            r = self.count
            self.count -= 1
            return r


for i in countdown(10):
    print(i)


# countdown generator
def countdown_gen(n):
    print("enter into countdown_gen")
    while n > 0:
        yield n
        n -= 1


m = countdown_gen(10)
print(m)
print(m.next())

# 结论：使用generator 函数 比创建一个支持iteration的对象更方便
# generator vs iterator 一次性的买卖

# generator 语法
# (expression for i in s if cond1
#            for j in t if cond2
#            ...
#            if condfinal)

log_str = '66.249.72.134 - ... "GET /index.html HTTP/1.1" 200 4447'
mda = log_str.rsplit(None, 1)
print(mda)
