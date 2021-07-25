# [lc1226 ][1]
当5个哲学家同时拿着左边或者 右边的叉子时，就会发生死锁。
死锁的四个必要条件：
- 互斥条件：一个资源在某一时间只能被一个进程持有，如果此时有其他的进程请求，只能等待。
- 请求和保持条件：进程在持有资源的情况下，又去申请别的资源，但是别的资源被另一个进程占有，此进程只能等待，同时不释放已占有的资源
- 不可剥夺条件：进程所获得的资源在未使用完毕之前，不能被其他进程强行夺走，即只能 由获得该资源的进程自己来释放（只能是主动释放)。
- 循环等待条件： 若干进程间形成首尾相接循环等待资源的关系。
```python
from threading import Lock, Semaphore
class DiningPhilosophers:
    def __init__(self):
        self.limit = Semaphore(4) # 限制最多4个人同时持有叉子
        self.ForkLocks = [Lock() for _ in range(5)] # 叉子锁

    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:

        right_lock = philosopher
        left_lock = (philosopher + 1) % 5
        self.limit.acquire() # 想吃饭

        # 尝试拿起叉子
        self.ForkLocks[right_lock].acquire()
        self.ForkLocks[left_lock].acquire()
        
        pickLeftFork()
        pickRightFork()
        eat()
        putRightFork()
        putLeftFork()

        # 放下叉子
        self.ForkLocks[right_lock].release()
        self.ForkLocks[left_lock].release()
        self.limit.release()
```

## 方法- 轮流进餐
```python

class DiningPhilosophers:
    def __init__(self):
        self.limit = Semaphore(1) # 限制最多4个人同时持有叉子

    def wantsToEat(self,
                   philosopher: int,
                   pickLeftFork: 'Callable[[], None]',
                   pickRightFork: 'Callable[[], None]',
                   eat: 'Callable[[], None]',
                   putLeftFork: 'Callable[[], None]',
                   putRightFork: 'Callable[[], None]') -> None:

        self.limit.acquire() # 想吃饭
        
        pickLeftFork()
        pickRightFork()
        eat()
        putRightFork()
        putLeftFork()
        self.limit.release()
```
# [1114. 按序打印][2]
我们提供了一个类：
```python
"""
三个不同的线程 A、B、C 将会共用一个 Foo 实例。
一个将会调用 first() 方法
一个将会调用 second() 方法
还有一个将会调用 third() 方法
请设计修改程序，以确保 second() 方法在 first() 方法之后被执行，third() 方法在 second() 方法之后被执行。
"""
public class Foo {
  public void first() { print("first"); }
  public void second() { print("second"); }
  public void third() { print("third"); }
}
```

```python
from threading import Lock
class Foo:
    def __init__(self):
        self.first_lock = Lock()
        self.second_lock = Lock()
        self.first_lock.acquire()
        self.second_lock.acquire()


    def first(self, printFirst: 'Callable[[], None]') -> None:
        
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.first_lock.release()


    def second(self, printSecond: 'Callable[[], None]') -> None:
        with self.first_lock:
            printSecond()
            self.second_lock.release()

        
        # printSecond() outputs "second". Do not change or remove this line.
        


    def third(self, printThird: 'Callable[[], None]') -> None:
        
        # printThird() outputs "third". Do not change or remove this line.
        with self.second_lock:
            printThird()
```

# [ 1115. 交替打印FooBar][3]
我们提供一个类
```python
"""
两个不同的线程将会共用一个 FooBar 实例。其中一个线程将会调用 foo() 方法，另一个线程将会调用 bar() 方法。

请设计修改程序，以确保 "foobar" 被输出 n 次。
"""
class FooBar {
  public void foo() {
    for (int i = 0; i < n; i++) {
      print("foo");
    }
  }

  public void bar() {
    for (int i = 0; i < n; i++) {
      print("bar");
    }
  }
}

```

```python
class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_lock = threading.Lock()
        self.bar_lock = threading.Lock()
        self.bar_lock.acquire()

    def foo(self, printFoo: 'Callable[[], None]') -> None:
        for i in range(self.n):
            
            # printFoo() outputs "foo". Do not change or remove this line.
            self.foo_lock.acquire()
            printFoo()
            self.bar_lock.release()


    def bar(self, printBar: 'Callable[[], None]') -> None:
        
        for i in range(self.n):
            
            # printBar() outputs "bar". Do not change or remove this line.
            self.bar_lock.acquire()
            printBar()
            self.foo_lock.release()
```

# [1117. H2O 生成][4]
```python
class H2O:
    def __init__(self):
        self.b = Barrier(3)
        self.h = Semaphore(2)
        self.o = Semaphore(1)

    def hydrogen(self, releaseHydrogen):
        with self.h:
            self.b.wait()
            releaseHydrogen()

    def oxygen(self, releaseOxygen):
        with self.o:
            self.b.wait()
            releaseOxygen()
```

[1]:	https://leetcode-cn.com/problems/the-dining-philosophers/
[2]:	https://leetcode-cn.com/problems/print-in-order/
[3]:	https://leetcode-cn.com/problems/print-foobar-alternately/
[4]:	https://leetcode-cn.com/problems/building-h2o/