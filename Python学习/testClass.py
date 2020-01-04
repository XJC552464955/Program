class Cat:
    def __init__(self,new_name): #构造函数
        self.name = new_name

    def __del__(self):  #析构函数
        print("销毁")

    def __str__(self): #打印对象时，需要显示的内容，默认不修改的时候返回对象和对象所在的地址
        return "我是小猫"


    def eat(self):
        print("mao")

Tom = Cat("Tom")

Tom.eat()

print(Tom)