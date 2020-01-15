class A(object):
    instance = None
    flag = False
    def __new__(cls, *args, **kwargs):
        #判断对象是否为空
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    #TODO 让初始化只执行一次
    def __init__(self):
        if not self.flag:
            print("a")
            self.flag = True

a = A()
print(a)
b = A()
print(b)