import pygame
from Python学习.飞机大战.plane_sprites import *

pygame.init()

class PlaneGame(object):
    '''飞机大战主游戏'''
    def __init__(self):
        '''游戏初始化方法'''
        print("游戏初始化")
        #1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #创建游戏结束画面
        self.canvas_over = CanvasOver(self.screen)

        #2.创建游戏时钟
        self.clock = pygame.time.Clock()

        #3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        #4.游戏bgm
        self.bg_music = pygame.mixer.Sound("./music/game_music.ogg")
        self.bg_music.set_volume(0.3)
        self.bg_music.play(-1)  #-1循环播放音乐

        #游戏结束
        self.game_over = False

        #分数对象
        self.score = GameSocre()

        #5.设置定时器时间
        pygame.time.set_timer(CREAT_ENEMY_EVENT,1000) #创建敌机
        pygame.time.set_timer(PLAYER_FIRE_EVENT, 500) #主角发射子弹

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
        #血条列表
        self.bars = []
        self.bars.append(self.player.bar)

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

            #6.结束刷新
            if self.game_over:
                self.canvas_over.update()

            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        '''事件监听'''
        for event in pygame.event.get():
            #判断是否退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == CREAT_ENEMY_EVENT:
                # print("敌机出场》》》")
                if self.game_over == False:
                    self.enemy = Eneny()
                    self.enemy_ground.add(self.enemy)
                    self.bars.append(self.enemy.bar)

            elif event.type == PLAYER_FIRE_EVENT:
                if self.game_over == False:
                    self.player.fire()
            # elif event.type == pygame.KEYDOWN and event.type == pygame.K_RIGHT:
            #     print("向右")
            else:
                if self.game_over == True:
                    flag = self.canvas_over.event_handler(event)
                    if flag == 1:
                        self.__start__()
                    elif flag == 0:
                        pygame.quit()
                        exit()

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
        # enemies = pygame.sprite.spritecollide(self.player,self.enemy_ground,True)
        # if len(enemies) > 0:
        #     self.player.kill()
        #     PlaneGame.__pygame_over()

        #1.子弹摧毁敌机
        for enemy in self.enemy_ground:
            for player in self.player_ground:
                for bullet in player.bullet_ground:
                    if pygame.sprite.collide_mask(bullet, enemy):  #这种碰撞检测可以精确到像素去掉alpha遮罩的情况
                        bullet.kill()
                        enemy.injury = bullet.hity
                        enemy.isboom = True
                        if enemy.bar.lenght <= 0:
                            self.enemy_ground.remove(enemy)
                            self.enemy_boom.add(enemy)

        #2.敌机撞到玩家
        for enemy in self.enemy_ground:
            if pygame.sprite.collide_mask(self.player,enemy):
                if enemy.num < 3:
                    enemy.bar.lenght = 0
                    self.player.injury = self.player.bar.value / 4

                    self.enemy_ground.remove(enemy)
                    self.enemy_boom.add(enemy)
                    enemy.isboom = True
                else:
                    self.player.bar.lenght = 0
                self.player.isboom = True

        #检查玩家是否死亡
        if not self.player.alive():
            self.player.rect.right = -10
            self.game_over = True

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

        self.bars_update()

        self.player.bullet_ground.update()
        self.player.bullet_ground.draw(self.screen)

        self.score_show()

    def bars_update(self):
        for bar in self.bars:
            if bar.lenght > 0:
                bar.update(self.screen)
            else:
                self.bars.remove(bar)

    #分数显示
    def score_show(self):
        score_font = pygame.font.Font("./fonts/STCAIYUN.ttf", 33)
        image = score_font.render("SCORE:" + str(int(self.score.getvalue())), False, color_gray)
        rect = image.get_rect()
        rect.bottom, rect.left = 700, 0
        self.screen.blit(image, rect)

    @staticmethod   #设置静态方法
    def __start__():
        print("游戏结束")
        # 创建游戏对象
        game = PlaneGame()

        # 启动游戏
        game.start_game()

if __name__ == '__main__':
    PlaneGame.__start__()