# New-style classes unify the concepts of class and type. If obj is an instance of a new-style class, type(obj) is the same as obj.__class__:

'''
在 Python 3 中，所有的类都是新式类。
因此，在 Python 3 中，可以互换地引用对象的类型和它的类。
'''


'''
请记住，在 Python 中，一切都是对象。类也是对象。
因此，一个类必须有一个类型。一个类的类型是什么？
请考虑以下内容。
'''
class A:
    pass

print(A.__class__)
print(type(A))


n = 5
d = {'x': 1, 'y': 2}

x = A()

for item in (n, d, x):
    print(item.__class__ is type(item))


######
# x的type 是A
# A的type 是type
# 一般来说，任何新式类的类型都是type
# type的类型也是type
print(type(x))
print(type(A))

"""
类型是一个元类，类是元类的实例。
就像一个普通的对象是一个类的实例一样，Python中的任何新式类，
从而Python 3中的任何类，都是类型元类的实例。
"""


"""
动态定义一个元类
"""

"""
内置的type()函数，当传递一个参数时，返回一个对象的类型。对于新式类来说，这通常与对象的__class__属性相同。
"""

'''
你也可以用三个参数-type(<name>, <bases>, <dct>)调用type()。

<name>指定了类的名称。这将成为该类的__name__属性。
<bases> 指定了类继承的基类的元组。这将成为该类的__bases__属性。
<dct> 指定了一个包含类主体定义的命名空间字典。这将成为类的__dict__属性。
以这种方式调用 type() 会创建一个新的类型元类实例。换句话说，它动态地创建了一个新的类。

在下面的每一个例子中，上面的代码段使用type()动态地定义了一个类，而下面的代码段则以通常的方式，使用class语句定义了这个类。在每种情况下，这两个代码段在功能上都是等价的。
'''
# 写法A
A = type('A', (), {})


# 写法B
class A:
    pass


print(type(A))

"""
现在用type的方式写一个类，继承自A，有一个属性attr=100
"""
Bar = type('Bar', (A, ), {'attr': 100})

x = Bar()
print(x.__class__.__bases__, x.attr)

# 上面的这种写法和下面的这种写法达到的效果是完全一样的
class Bar(A):
    attr = 100
    pass

class Bar1(A):
    def __init__(self):
        self.attr = 100

# 注意区分attr 放到__init__ 和 不放到__init__中的区别
# 一个是类的属性，一个是实例的属性
# 所以 'attr' in Bar.__dict__
# 但是并不在 Bar().__dict__

print(f"Bar dict: {Bar().__dict__} {Bar().attr}")

print(f"Bar1 dict: {Bar1.__dict__}")


models = {}
def model(cls):
    models[cls.__name__] = cls
    return cls

@model
class TestModel(object):
    pass

print(models)
# 但是继承自TestModel的model 并不会放到models，要想让继承自TestModel的子类也放入到models中，就要利用metaclass的能力

class TestB(TestModel):
    pass

print(models)


## 用meta实现

class ModelMetaClass(type):
    def __new__(meta, name, bases, attrs):
        models[name] = cls = type.__new__(meta, name, bases, attrs)
        return cls

class TestA(metaclass=ModelMetaClass):
    pass

class TestB(metaclass=ModelMetaClass):
    pass

print(models)



