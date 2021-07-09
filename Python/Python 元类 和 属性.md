Python 元类 和 属性
在python 中一切都是对象，类也是对象。
类的类型是type，也就是元类。
```python
class A:
    pass

print(A.__class__)  # ==>  type<class 'type'>
print(type(A)) # ==> <class 'type'>
```
type 是元类，普通类型都是元类的实例。
内置的type()函数，当传递一个参数时，返回一个对象的类型。对于新式类来说，这通常与对象的__class__属性相同。
你也可以用三个参数`-type(<name>, <bases>, <dct>)`调用`type()`。

`<name>`指定了类的名称。这将成为该类的`__name__`属性。
`<bases>` 指定了类继承的基类的元组。这将成为该类的`__bases__`属性。
`<dct>` 指定了一个包含类主体定义的命名空间字典。这将成为类的`__dict__`属性。
以这种方式调用` type() `会创建一个新的类型元类实例。换句话说，它动态地创建了一个新的类。

在下面的每一个例子中，上面的代码段使用`type()`动态地定义了一个类，而下面的代码段则以通常的方式，使用class语句定义了这个类。在每种情况下，这两个代码段在功能上都是等价的。
```python
# 写法A
A = type('A', (), {})


# 写法B
class A:
    pass


print(type(A))

```

现在用type的方式写一个类，继承自A，有一个属性attr=100
```python
Bar = type('Bar', (A, ), {'attr': 100})

x = Bar()
print(x.__class__.__bases__, x.attr)

```
上面的这种写法和下面的这种写法达到的效果是完全一样的
```python
class Bar(A):
    attr = 100
```
注意和这种写法区分开：
```python
class Bar1(A):
    def __init__(self):
        self.attr = 100

```

注意区分attr 放到`__init__` 和 不放到`__init__`中的区别
 一个是类的属性，一个是实例的属性
所以 `attr` in `Bar.__dict__`
但是并不在` Bar().__dict__`
