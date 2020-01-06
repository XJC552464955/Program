class A:
    def eat(self):
        print("A")
    def a(self):
        print(1)

class B:
    def eat(self):
        print("B")

class C(A,B):
    pass

c = A()
print(C.mro())