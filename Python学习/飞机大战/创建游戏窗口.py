import pygame

size = (weidth, height) = (480,700)  #设置屏幕大小
screen = pygame.display.set_mode(size)   #绘制屏幕

bg = pygame.image.load("./images/background.png") #加载背景图像
#加载player
player = pygame.image.load("./images/me1.png")

screen.blit(bg, (0, 0))  # 绘制图像
screen.blit(player, (200, 500))
pygame.display.update()  # 更新屏幕显示,可以在所有绘制工作完成之后，同意调用update方法

global keep_going
keep_going = True  #循环变量
while keep_going:
    pass

pygame.quit()