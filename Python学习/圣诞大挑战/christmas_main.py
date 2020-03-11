import pygame
from  Python学习.圣诞大挑战.chrismas_sprite import *

pygame.init()

class ChristmasGame(object):
    '''圣诞大挑战主程序'''
    def __init__(self):
        #游戏初始化
        #1.屏幕
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        #2.调用资源设置方法
        self.__create_sprite()


    def start_game(self):
        #游戏开始
        while True:
            #1.游戏时钟

            #2.精灵更新
            self.update_sprite()

            #3.碰撞检测

            #4.事件监听

            #刷新屏幕
            pygame.display.update()

    def __create_sprite(self):
        #创建背景精灵组
        bg = BackGround()
        self.bgGround = pygame.sprite.Group(bg)


    def update_sprite(self):
        #刷新背景
        self.bgGround.update()
        self.bgGround.draw(self.screen)

    @staticmethod
    def __start__():
        # 实例化游戏对象
        game = ChristmasGame()
        # 开始游戏
        game.start_game()

if __name__ == '__main__':
    #程序入口
    ChristmasGame.__start__()