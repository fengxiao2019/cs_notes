res = ['0', 'A', 'B', 'C', 'D', 'E']


class Tree(object):
    def __int__(self, val):
        self.left = None
        self.right = None
        self. val = val

def build_tree(node_queue, data_list):
    i = 0
    root = data_list[i]
    node_queue.append(root)
    i += 1
    while node_queue and i < len(data_list):
        node = node_queue.pop(0)
        node.left = Tree(data_list[i])
        i += 1
        node_queue.append(node.left)
        if i >= len(data_list):
            break
        node.right = data_list[i]
        i += 1
        node_queue.append(node.right)



class MyClassDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('preprocessing', args)
        if args:
            if isinstance(args[0], int):
                a = list(args)
                a[0] += 5
                args = tuple(a)
                print('preprocess OK', args)
        r = self.func(*args, **kwargs)
        print('postprocessing', r)
        r += 7
        return r


@MyClassDecorator
def my_function(*args, **kwargs):
    print('call my_function', args, kwargs)
    return 3


# 实现单例模式

##1 decorator

import threading


def synchronized(func):
    func.__lock__ = threading.Lock()
    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return wrapper

# 实现一个method类型的锁
def synchronized_method(func):
    func.__lock__ = threading.Lock()
    def wrapper(self, *args, **kwargs):
        with self.lock:
            return func(self, *args, **kwargs)
    return wrapper

class Singleton(type):
    instances = {}
    lock = threading.Lock()
    def __new__(cls, *args, **kwargs):

        if cls not in Singleton.instances:
            with Singleton.lock:
                if cls not in Singleton.instances:
                    Singleton.instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return Singleton.instances[cls]


## 观察者模式

class Visitor():
    def __init__(self):
        self.visitors = []

    def visit(self):
        pass

    def accept(self, ):



class A(metaclass=Singleton):
    pass

print(id(A()))
print(id(A()))
id(A()) == id(A())
print(A.__name__)

