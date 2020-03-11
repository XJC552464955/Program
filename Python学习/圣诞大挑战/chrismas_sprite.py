import pygame

pygame.init()

SCREEN_RECT = pygame.Rect(0,0,960,720)

#刷新频率


class GamePrite(pygame.sprite.Sprite):
    def __init__(self,image_path, speedX = 0, speedY = 0):
        #调用父类构造
        super().__init__()

        #加载图片，检测图片是否加载完成
        try:
            self.image = pygame.image.load(image_path)
            self.rect = self.image.get_rect()
        except:
            print("没有找到图片")

        self.speedX = speedX
        self.speedY = speedY

    def update(self, *args):
        self.rect.y += self.speedY
        self.rect.x += self.speedX

class BackGround(GamePrite):
    def __init__(self):
        super().__init__("./images/bg.png")

    def update(self, *args):
        super().update()


