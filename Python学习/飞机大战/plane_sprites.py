import random
import pygame

pygame.init()

#分数
SOCRE = 0

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#color
color_red = (255, 0, 0)
color_blue = (30,144,255)
color_green = (0,255,0)
color_gray = (251, 255, 242)
#刷新的帧率
FRAME_PER_SEC = 60
#创建敌机的定时常量
CREAT_ENEMY_EVENT = pygame.USEREVENT
#player子弹事件
PLAYER_FIRE_EVENT = pygame.USEREVENT + 1

class GameSocre(object):
    global SOCRE
    def     __init__(self):
        self.socre = 0
    def getvalue(self):
        self.socre = SOCRE
        return self.socre

class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''

    def __init__(self, image_name, speedx=0, speedy=1):
        #调用父类的初始化方法
        super().__init__()

        #定义对象属性
        try:
            self.image = pygame.image.load(image_name)
            self.rect = self.image.get_rect()
            self.speedx = speedx
            self.speedy = speedy
            self.injury = 1 #伤害值
            self.index = 0 #记帧数变量
            self.bar = bloodline(color_blue,self.rect.x,self.rect.y-10,self.rect.width)
        except:
            print("没找到图片")

    def update(self):
        #在屏幕的垂直方向上移动
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.bar.x = self.rect.x
        self.bar.y = self.rect.y - 10

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
        self.speedy = random.randrange(1,3)

        #3.指定敌机的初始随机位置
        self.rect.bottom = 0
        self.rect.x = random.randint(10,SCREEN_RECT.right-self.rect.width//2-40)
        self.enemy_boom = pygame.sprite.Group()

        #4.爆炸效果
        self.isboom = False
        self.index = 1

        #5.音效
        if self.num == 1:
            #pygame.mixer.Sound()加载声音资源
            self.music_boom = pygame.mixer.Sound("./music/enemy1_down.wav")
        elif self.num == 2:
            self.music_boom = pygame.mixer.Sound("./music/enemy2_down.wav")

        #6.血条
        if self.num == 1:
            self.bar = bloodline(color_blue,self.rect.x,self.rect.y,self.rect.width)
        elif self.num == 2:
            self.bar = bloodline(color_blue,self.rect.x,self.rect.y,self.rect.width, 3, 4)

        #子弹精灵组
        self.bullets = pygame.sprite.Group()

    def fire(self):
        for i in range(0,2):
            #创建子弹
            bullet = Bullet(0, random.randint(self.speedy + 1,self.speedy + 3))
            #设置精灵位置
            bullet.rect.bottom = self.rect.bottom + i * 20 #枪口发射
            bullet.rect.centerx = self.rect.centerx  #居中

            #将子弹呢添加到精灵组
            self.bullets.add(bullet)


    def update(self):
        global SOCRE
        #1. 调用父类方法，保持垂直方向飞行
        super().update()

        #2.判断是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出了屏幕")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()
            self.bar.lenght = 0

        if self.isboom:  #爆炸控制
            self.bar.lenght -= self.injury * self.bar.weight
            if self.bar.lenght <= 0: #检查血量值，仍有血量不需要爆炸将变量设为False
                #播放音乐
                if self.index == 1:
                    self.music_boom.play()
                #爆炸
                if self.index < 17:   #多执行几遍让爆炸显示出来
                    self.image = pygame.image.load(
                        "./images/enemy" + str(self.num) + "_down" + str(self.index//4) + ".png")
                    # 整除4是减慢爆炸的速度，如果按照update的频率60hz就太快了
                    self.index+=1
                else:
                    self.kill()
                    SOCRE += self.bar.value
            else:
                self.isboom = False


    def __del__(self):
        print("敌机销毁",self.rect)


class Player(GameSprite):
    def __init__(self):
        #1.调用父类方法，设置image
        super().__init__("./images/me1.png")

        self.num = 0
        #2.设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120

        #创建子弹精灵组
        self.bullet_ground = pygame.sprite.Group()

        #玩家血条
        self.bar = bloodline(color_green,0,700,480,8,10)

        #爆炸
        self.isboom = False
        self.index1 = 1 #控制喷气动画速度
        self.index2 = 0 #控制爆炸动画速度

        #音效
        self.music_down = pygame.mixer.Sound("./music/me_down.wav")
        self.music_upgrade = pygame.mixer.Sound("./music/upgrade.wav")
        self.music_degrade = pygame.mixer.Sound("./music/supply.wav")

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #检测x边缘
        if self.rect.left < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        #检测y边缘
        if self.rect.top < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

        #英雄喷气动画
        self.image = pygame.image.load("./images/me" + str((self.index1//6) % 2 + 1) + ".png")  #取整6是减缓动画速度
        self.index1 += 1

        #爆炸动画
        if self.isboom:
            self.bar.lenght -= self.injury * self.bar.weight   #计算实时血条长度，损伤*每滴血的距离即为掉血量
            if self.bar.lenght <= 0:
                if self.index2 <= 16:
                    self.image = pygame.image.load("./images/me_destroy_" + str(self.index2 % 5) + ".png")
                    self.index2 += 1
                else:
                    self.kill()
            else:
                self.isboom = False

    def player_move(self,speedx=0,speedy=0):
        self.speedx = speedx
        self.speedy = speedy


    def fire(self):
        # print("发射子弹")
        bullet = Bullet()
        bullet.rect.bottom = self.rect.top
        bullet.rect.centerx = self.rect.centerx
        self.bullet_ground.add(bullet)

class Bullet(GameSprite):
    def __init__(self,color=1, speedx=0, speedy =-2):
        self.hity = color #设置子弹伤害
        self.music_shoot = pygame.mixer.Sound("./music/bullet.wav")
        self.music_shoot.set_volume(0.3)  #播放速度
        if color > 0: #只让玩家发子弹响
            self.music_shoot.play()
        super().__init__("./images/bullet"+ str(color) +".png",speedx,speedy)

    def update(self):
        super().update()
        if self.rect.bottom < 0 or self.rect.y > 700:
            self.kill()

    def __del__(self):
        # print("子弹销毁")
        pass

class bloodline(object):
    '''血条UI'''
    def __init__(self,color, x, y, lenght, width = 2, value = 2):
        self.color = color
        self.x = x
        self.y = y
        self.lenght = lenght  #实时线长
        self.width = width  #线宽
        self.value = value * 1.0  #血量,用浮点型
        self.weight = lenght / value  #每滴血表示的距离
        self.color_init = color   #血条默认颜色

    def update(self, canvas):
        if self.lenght <= self.value * self.weight / 2:
            #实时线长小于一半血量的距离时红色
            self.color = color_red
        else:
            self.color = self.color_init
        #画出线条
        self.bar_rect = pygame.draw.line(canvas,self.color,(self.x,self.y),(self.x + self.lenght, self.y), self.width)

class CanvasOver(object):
    #初始化结束界面图片与图片位置
    def __init__(self,screen):
        self.img_again = pygame.image.load("./images/again.png")
        self.img_over = pygame.image.load("./images/gameover.png")
        self.rect_again = self.img_again.get_rect()
        self.rect_over = self.img_over.get_rect()
        self.rect_again.centerx = self.rect_over.centerx = SCREEN_RECT.centerx
        self.rect_again.bottom = SCREEN_RECT.centery
        self.rect_over.y = self.rect_again.bottom + 20
        self.screen = screen

    # 检测有没有点击按钮
    def event_handler(self,event):
            pos = pygame.mouse.get_pos()
            if self.rect_again.left < pos[0] < self.rect_again.right \
                and self.rect_again.top < pos[1] < self.rect_again.bottom:
                return 1
            elif self.rect_over.left < pos[0] < self.rect_over.right and \
                    self.rect_over.top < pos[1] < self.rect_over.bottom:
                return 0

    #更新显示
    def update(self):
        self.screen.blit(self.img_over,self.rect_over)
        self.screen.blit(self.img_again,self.rect_again)
        score_font = pygame.font.Font("./fonts/STCAIYUN.ttf",50)
        #render将文字绘制到surface，参数一 text, 参数二antialias, 参数三color, 参数四background=None
        image = score_font.render("SCORE:" + str(int(SOCRE)),True,color_gray,None)
        rect_image = image.get_rect()
        rect_image.centerx, rect_image.bottom = SCREEN_RECT.centerx, self.rect_again.top - 20
        self.screen.blit(image, rect_image)