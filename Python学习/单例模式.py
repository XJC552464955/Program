class A(object):
    instance = None
    def __new__(cls, *args, **kwargs):
        #判断对象是否为空
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass

a = A()
print(a)
b = A()
print(b)