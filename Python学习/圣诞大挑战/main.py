import random
import pygame

pygame.init()

#屏幕大小
SCREEN_RECT = pygame.Rect(0,0,960,720)

#屏幕刷新频率
FRAME_PER_SEC = 60

#敌人发射事件常量
ENEMY_FIRE_EVENT = pygame.USEREVENT

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,path,speedx = 0,speedy = 0):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy

    def update(self, *args):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class BackGround(GameSprite):
    def __init__(self):
        super().__init__("./images/bg.png")

    def update(self, *args):
        super().update()

class Eneny(GameSprite):
    def __init__(self):
        #指定图片与移动
        super().__init__("./images/enemy.png", 3, 0)
        #翻转图片
        self.image = pygame.transform.flip(self.image, 1, 0)
        #缩放图片
        self.image = pygame.transform.smoothscale(self.image,(100,80))
        #重新获取矩形区间
        self.rect = self.image.get_rect()
        #指定位置
        self.rect.top = 0
        self.rect.left = 0
        #创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()
        #创建礼物精灵组
        self.gift_group = pygame.sprite.Group()

    def update(self, *args):
        #调用父类构造
        super().update()
        #判断是否到达边缘
        if self.rect.right > SCREEN_RECT.right or self.rect.left < 0:
            #反转图片
            self.image = pygame.transform.flip(self.image,1,0)
            #改变移动方向
            self.speedx *= -1

    def fire(self):
        bullet = Bullet()
        bullet.rect.center = self.rect.center
        if bullet.type == bullet.bullet_type[0]:
            self.bullet_group.add(bullet)
        else:
            self.gift_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        self.bullet_type = ("./images/enemy_bullet_tang.png","./images/enemy_bullet_xueqiu0.png")
        self.type = self.bullet_type[random.randint(0,len(self.bullet_type)-1)]
        super().__init__(self.type,0,5)
        self.image = pygame.transform.smoothscale(self.image,(60,60))
        self.rect = self.image.get_rect()

        #爆炸动画索引
        self.index = 0
        #爆炸控制
        self.isBoom = False

    def update(self, *args):
        super().update()
        if self.rect.top > SCREEN_RECT.bottom:
            self.kill()

        if self.isBoom:
            if self.index <= 8:
                self.image = pygame.image.load("./images/enemy_bullet_xueqiu" + str(self.index//4) + ".png")
                self.image = pygame.transform.smoothscale(self.image,(60,60))
                self.index += 1
            else:
                self.kill()

    def __del__(self):
        print("子弹消失")

class Player(GameSprite):
    def __init__(self):
        super(Player, self).__init__("./images/player.png")
        self.image = pygame.transform.smoothscale(self.image, (100,100))
        self.rect = self.image.get_rect()

        #设置位置
        self.rect.bottom = SCREEN_RECT.bottom
        self.rect.centerx = SCREEN_RECT.centerx

    def update(self, *args):
        super(Player, self).update()
        self.rect.x += self.speedx
        if self.rect.left < SCREEN_RECT.left:
            self.rect.left = SCREEN_RECT.left
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def move(self,speedx):
        self.speedx = speedx


class GameStart():
    def __init__(self):
        #1.初始化屏幕
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.创建时钟
        self.clock = pygame.time.Clock()

        #3.创建精灵组
        self._creat_sprite()

        #4.设置定时器
        pygame.time.set_timer(ENEMY_FIRE_EVENT,random.randint(1000,2000))

        #5.游戏结束
        self.game_over = False

    def start_game(self):
        while True:
            #1.刷新时钟
            self.clock.tick(FRAME_PER_SEC)

            #2.事件检测
            self._event_handle()

            #3.碰撞检测
            self._check_collider()

            #4.更新精灵组
            self._update_sprite()

            #5.更新显示
            pygame.display.update()

    def _creat_sprite(self):
        #创建背景
        bg = BackGround()
        self.back_ground = pygame.sprite.Group(bg)

        #创建敌人精灵
        self.enemy = Eneny()
        self.enemy_group = pygame.sprite.Group(self.enemy)

        #创建玩家精灵
        self.player = Player()
        self.player_group = pygame.sprite.Group(self.player)

    def _update_sprite(self):
        #1.背景刷新
        self.back_ground.update()
        self.back_ground.draw(self.screen)

        #2.敌人刷新
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        #3.敌人子弹更新
        self.enemy.bullet_group.update()
        self.enemy.bullet_group.draw(self.screen)
        self.enemy.gift_group.update()
        self.enemy.gift_group.draw(self.screen)

        #4.玩家刷新
        self.player_group.update()
        self.player_group.draw(self.screen)

    def _event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == ENEMY_FIRE_EVENT:
                #生成子弹物品
                self.enemy.fire()
                #重新设置定时器时间
                pygame.time.set_timer(ENEMY_FIRE_EVENT, random.randint(1000, 2000))
            else:
                if self.game_over:
                    pygame.quit()
                    exit()

            #获取按键事件
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_a]:
                self.player.move(-3)
            elif key_pressed[pygame.K_d]:
                self.player.move(3)
            else:
                self.player.move(0)

    def _check_collider(self):
        for gift in self.enemy.gift_group:
            if pygame.sprite.collide_mask(gift,self.player):
                gift.isBoom = True
                self.game_over = True


if __name__ == '__main__':
    game = GameStart()
    game.start_game()