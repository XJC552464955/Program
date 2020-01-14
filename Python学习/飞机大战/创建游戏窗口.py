import pygame
from Python学习.飞机大战.plane_sprites import *

size = (weidth, height) = (480,700)  #设置屏幕大小
screen = pygame.display.set_mode(size)   #绘制屏幕

bg = pygame.image.load("./images/background.png") #加载背景图像
#加载player
player = pygame.image.load("./images/me1.png")
#创建时钟对象
clock = pygame.time.Clock()

here_rect = player.get_rect(left=190, top=500)   #here_rect = pygame.Rect(200, 500,102,126)   手动获取矩形区域

#创建敌人的精灵
enemy = GameSprite("./images/enemy1.png")
enemy1 = GameSprite("./images/enemy1.png", 2)

#创建敌人精灵组
enemy_groud = pygame.sprite.Group(enemy, enemy1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 可以指定循环体内部的代码执行的频率 和休眠的区别在于一个控制时间，一个控制每秒运行次数
    clock.tick(60)

    #修改飞机的位置
    here_rect.y -= 1

    if here_rect.y < -126:
        here_rect.y = 700


    #调用blit方法绘制图像
    screen.blit(bg, (0, 0))  # 绘制背景图像到surface
    screen.blit(player,here_rect)  # 绘制角色图像
    pygame.display.update()  # 更新屏幕显示,可以在所有绘制工作完成之后，同意调用update方法

    #让精灵组调用update()和draw()方法
    #uodate - 让组中所有精灵更新位置
    enemy_groud.update()
    enemy_groud.draw(screen)