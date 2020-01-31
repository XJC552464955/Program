import pygame
from Python学习.飞机大战.plane_sprites import *

class PlaneGame(object):
    '''飞机大战主游戏'''
    def __init__(self):
        '''游戏初始化方法'''
        print("游戏初始化")
        #1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.创建游戏时钟
        self.clock = pygame.time.Clock()

        #3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        #4.设置定时器时间-创建敌机
        pygame.time.set_timer(CREAT_ENEMY_EVENT,1000)
        pygame.time.set_timer(PLAYER_FIRE_EVENT, 500)

    def __create_sprites(self):
        '''精灵生成方法'''
        #创建背景精灵和精灵组
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_ground = pygame.sprite.Group(bg1,bg2)
        #创建敌机精灵组
        self.enemy_ground = pygame.sprite.Group()
        #创建玩家和玩家精灵组
        self.player = Player()
        self.player_ground = pygame.sprite.Group(self.player)
        #创建爆炸组
        self.enemy_boom = pygame.sprite.Group()

    def start_game(self):
        '''游戏启动方法'''
        print("游戏开始...")
        while True:
            #1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #2.事件监听
            self.__event_handler()
            #3.碰撞检测
            self.__check_collider()
            #4.更新、绘制精灵组
            self.__update_sprites()
            #5.更新显示
            pygame.display.update()

    def __event_handler(self):
        '''事件监听'''
        for event in pygame.event.get():
            #判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__pygame_over()
            elif event.type == CREAT_ENEMY_EVENT:
                # print("敌机出场》》》")
                self.enemy = Eneny()
                self.enemy_ground.add(self.enemy)
            elif event.type == PLAYER_FIRE_EVENT:
                self.player.fire()
            # elif event.type == pygame.KEYDOWN and event.type == pygame.K_RIGHT:
            #     print("向右")

        #使用键盘模块提供的方法
        key_pressed = pygame.key.get_pressed()
        #判断元组中对应的按键索引值
        if key_pressed[pygame.K_RIGHT]:
            # print("向右移动")
            self.player.player_move(5,0)
        elif key_pressed[pygame.K_LEFT]:
            self.player.player_move(-5,0)
        elif key_pressed[pygame.K_UP]:
            self.player.player_move(0, -5)
        elif key_pressed[pygame.K_DOWN]:
            self.player.player_move(0,5)
        else:
            self.player.player_move(0,0)

    def __check_collider(self):
        # '''碰撞'''
        # #groupcollide检测两个精灵组的碰撞，第三个参数控制第一个精灵组是否删除，第四个参数控制第二个精灵组
        # pygame.sprite.groupcollide(self.enemy_ground,self.player.bullet_ground,True,True)
        #spritecollide检测某个精灵和精灵组的碰撞,第三个参数控制精灵组是否删除
        #1.子弹摧毁敌机
        for enemy in self.enemy_ground:
            for player in self.player_ground:
                for player_bullet in self.player.bullet_ground:
                    if pygame.sprite.collide_mask(player_bullet, enemy):  #这种碰撞检测可以精确到像素去掉alpha遮罩的情况
                        player_bullet.kill()
                        enemy.isboom = True
                        self.enemy_ground.remove(enemy)
                        self.enemy_boom.add(enemy)

        enemies = pygame.sprite.spritecollide(self.player,self.enemy_ground,True)
        if len(enemies) > 0:
            self.player.kill()
            PlaneGame.__pygame_over()

    def __update_sprites(self):
        '''更新精灵'''
        self.back_ground.update()
        self.back_ground.draw(self.screen)

        self.enemy_ground.update()
        self.enemy_ground.draw(self.screen)

        self.enemy_boom.update()
        self.enemy_boom.draw(self.screen)

        self.player_ground.update()
        self.player_ground.draw(self.screen)

        self.player.bullet_ground.update()
        self.player.bullet_ground.draw(self.screen)


    @staticmethod   #设置静态方法
    def __pygame_over():
        print("游戏结束")
        pygame.quit()
        exit()

if __name__ == '__main__':
    #创建游戏对象
    game = PlaneGame()

    #启动游戏
    game.start_game()