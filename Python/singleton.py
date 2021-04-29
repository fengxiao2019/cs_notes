from threading import Lock

class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        cls.lk = Lock()
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls.lk:
                if cls.__instance is None:
                    cls.__instance = super().__call__(*args, **kwargs)

        return cls.__instance


class Spam(metaclass=Singleton):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

a = Spam()
b = Spam()
c = Spam()
print(a is b is c)


class Singleton1(object):
    __singleton_instance = None
    __singleton_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__singleton_instance is None:
            with cls.__singleton_lock:
                if cls.__singleton_lock is None:
                    cls.__singleton_instance = super().__new__(cls, *args, **kwargs)
        return cls.__singleton_instance

a = Singleton1()
b = Singleton1()
c = Singleton1()
print(a is b is c)



class SingletonM(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Log(metaclass=SingletonM):
    pass

a = Log()
b = Log()

print(a is b)