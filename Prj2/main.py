import os
import pygame
import random

pygame.init()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Puck(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("Black"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        while self.vx == 0:
            self.vx = random.randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, bita):
            self.vx = -self.vx
            self.vy = -self.vy


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if y2 == 10:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2, 10])
        else:
            self.add(vertical_borders)
            self.image = pygame.Surface([10, y2])
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x1, y1, x2, y2)


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

size = width, height = 1000, 500
speed = 4
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Аэрохоккей')
clock = pygame.time.Clock()

bita1_image = load_image('bita1.png', -1)
bita1 = pygame.sprite.Sprite(all_sprites)
bita1.image = bita1_image
bita1.rect = bita1.image.get_rect()
bita = pygame.sprite.Group()
bita1.rect.x = 100
bita1.rect.y = 190

Border(40, 20, size[0] - 80, 10)
Border(40, size[1] - 40, size[0] - 80, 10)
Border(40, 20, 10, 100)
Border(40, 370, 10, 100)
Border(size[0] - 40, 20, 10, 100)
Border(size[0] - 40, 370, 10, 100)

Puck(random.randint(15, 20), 485, 250)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_s] and bita1.rect.y <= 360:
            bita1.rect.top += speed
        elif key[pygame.K_w] and bita1.rect.y >= 30:
            bita1.rect.top -= speed
        elif key[pygame.K_a] and bita1.rect.x >= 40:
            bita1.rect.left -= speed
        elif key[pygame.K_d] and bita1.rect.x <= 370:
            bita1.rect.left += speed
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
