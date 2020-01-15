import pygame
from Python学习.飞机大战.plane_sprites import *

#屏幕大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)

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

    def __create_sprites(self):
        '''精灵生成方法'''
        pass

    def start_game(self):
        '''游戏启动方法'''
        print("游戏开始...")
        while True:
            #1.设置刷新帧率
            self.clock.tick(60)
            #2.事件监听
            self.__event_handler()
            #3.碰撞检测
            self.__check_collider()
            #4.更新、绘制精灵组
            self.__update_sprites()
            #5.更新显示
            pygame.display.update()
            pass

    def __event_handler(self):
        '''事件监听'''
        for event in pygame.event.get():
            #判断是否退出游戏
            if event.type == pygame.quit():
                PlaneGame.__pygame_over()


    def __check_collider(self):
        '''碰撞'''
        pass

    def __update_sprites(self):
        '''更新精灵'''
        pass

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