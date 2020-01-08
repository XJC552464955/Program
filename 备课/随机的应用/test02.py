import turtle
import random

pen = turtle.Pen()

pen.speed(0)
turtle.bgcolor("black")

colors = ["red","blue","yellow","orange"]

for i in range(100):
    x = random.randrange(-turtle.window_width()//2,turtle.window_width()//2)
    y = random.randrange(-turtle.window_height()//2,turtle.window_height()//2)
    pen.color(random.choice(colors))
    pen.penup()
    pen.setpos(x,y)
    pen.pendown()
    for j in range(random.randrange(20,50)):
        pen.forward(j)
        pen.right(91)