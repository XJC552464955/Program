import random
import pygame

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#刷新的帧率
FRAME_PER_SEC = 60
#创建敌机的定时常量
CREAT_ENEMY_EVENT = pygame.USEREVENT
#player子弹事件
PLAYER_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''

    def __init__(self, image_name, speed=1):
        #调用父类的初始化方法
        super().__init__()

        #定义对象属性
        try:
            self.image = pygame.image.load(image_name)
            self.rect = self.image.get_rect()
            self.speed = speed
        except:
            print("没找到图片")

    def update(self):
        #在屏幕的垂直方向上移动
        self.rect.y += self.speed

class BackGround(GameSprite):
    '''游戏背景精灵'''
    def __init__(self,is_alt = False):
        #调用父类方法，完成精灵创建
        super().__init__("./images/background.png")

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        #调用父类的方法实现
        #T判断是否移除屏幕
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height

class Eneny(GameSprite):
    def __init__(self, num=1):
        self.num = num   #记录敌机图片
        #1.调用父类方法创建敌机精灵,同时指定敌机图片
        super().__init__("./images/enemy"+str(num)+".png")
        #2.指定敌机的初始速度
        self.speed = random.randrange(1,3)

        #3.指定敌机的初始随机位置
        self.rect.bottom = 0
        self.rect.x = random.randint(10,SCREEN_RECT.right-self.rect.width//2-20)
        self.enemy_boom = pygame.sprite.Group()

        #4.爆炸效果
        self.isboom = False
        self.index = 1

    def update(self):
        #1. 调用父类方法，保持垂直方向飞行
        super().update()

        #2.判断是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出了屏幕")
            self.kill()

        if self.isboom:  #爆炸控制
            if self.index < 17:   #多执行几遍让爆炸显示出来
                self.image = pygame.image.load(
                    "./images/enemy" + str(self.num) + "_down" + str(self.index//4) + ".png")
                # 整除4是减慢爆炸的速度，如果按照update的频率60hz就太快了
                self.index+=1
            else:
                self.kill()

    def __del__(self):
        print("敌机销毁",self.rect)


class Player(GameSprite):
    def __init__(self):
        #1.调用父类方法，设置image
        super().__init__("./images/me1.png")
        #2.设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120

        #创建子弹精灵组
        self.bullet_ground = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
    def fire(self):
        # print("发射子弹")
        bullet = Player_Bullet()
        bullet.rect.bottom = self.rect.top
        bullet.rect.centerx = self.rect.centerx
        self.bullet_ground.add(bullet)

class Player_Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png",-2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("子弹销毁")
        pass