import turtle

pen = turtle.Pen()

pen.color("red")

for j in range(4):
    #⚪
    pen.circle(50)
    #画完旋转
    pen.right(90)
    #画正方形
    for i in range(4):
        pen.forward(50)
        pen.right(90)

turtle.done()