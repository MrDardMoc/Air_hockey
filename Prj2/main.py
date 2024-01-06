import os
import pygame
import random

pygame.init()


def movement(key):
    if key[pygame.K_s] and bita1.rect.y <= 400:
        bita1.rect.top += speed
    if key[pygame.K_w] and bita1.rect.y >= 30:
        bita1.rect.top -= speed
    if key[pygame.K_a] and bita1.rect.x >= 50:
        bita1.rect.left -= speed
    if key[pygame.K_d] and bita1.rect.x <= 440:
        bita1.rect.left += speed
    if (key[pygame.K_DOWN] or key[pygame.K_k]) and bita2.rect.y <= 400:
        bita2.rect.top += speed
    if (key[pygame.K_UP] or key[pygame.K_i]) and bita2.rect.y >= 30:
        bita2.rect.top -= speed
    if (key[pygame.K_LEFT] or key[pygame.K_j]) and bita2.rect.x >= 500:
        bita2.rect.left -= speed
    if (key[pygame.K_RIGHT] or key[pygame.K_l]) and bita2.rect.x <= 900:
        bita2.rect.left += speed


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


class AnimatedPuck(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.vx = 0
        self.vy = 0
        self.flag = 0
        self.puck_speed = [-7, -6, -5, 5, 6, 7]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if (((bita1.rect.x != 100 or bita1.rect.y != 220) or (bita2.rect.x != 850 or bita2.rect.y != 220))
                and self.flag != 1):
            self.flag = 1
            self.vx = random.choice(self.puck_speed)
            self.vy = random.choice(self.puck_speed)
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, bits):
            if (bita1.rect.top < self.rect.top and bita1.rect.left < self.rect.left or
                    bita1.rect.top > self.rect.top and bita1.rect.left < self.rect.left):
                self.vx = -self.vx
            elif (bita1.rect.top < self.rect.top and bita1.rect.left > self.rect.left or
                    bita1.rect.top > self.rect.top and bita1.rect.left > self.rect.left):
                self.vy = -self.vy
            else:
                self.vx = -self.vx
                self.vy = -self.vy
            print(bita1.rect.top - self.rect.top)
            print(bita1.rect.left - self.rect.left)


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
bits = pygame.sprite.Group()

size = width, height = 1000, 500
speed = 4
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Аэрохоккей')
clock = pygame.time.Clock()

radius = 30
bita1_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
pygame.draw.circle(bita1_image, pygame.Color("Red"), (radius, radius), radius)
bita1 = pygame.sprite.Sprite(bits)
bita1.image = bita1_image
bita1.rect = bita1.image.get_rect()
bita1.rect.x = 100
bita1.rect.y = 220

bita2_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
pygame.draw.circle(bita2_image, pygame.Color("Blue"), (radius, radius), radius)
bita2 = pygame.sprite.Sprite(bits)
bita2.image = bita2_image
bita2.rect = bita2.image.get_rect()
bita2.rect.x = 850
bita2.rect.y = 220

all_sprites.add(bits)

height_vert_bord = random.randint(0, 100)
Border(40, 20, size[0] - 80, 10)
Border(40, size[1] - 40, size[0] - 80, 10)
Border(40, 20, 10, height_vert_bord)
Border(40, 370 + (100 - height_vert_bord), 10, height_vert_bord)
Border(size[0] - 40, 20, 10, height_vert_bord)
Border(size[0] - 40, 370 + (100 - height_vert_bord), 10, height_vert_bord)

AnimatedPuck(load_image("circle_der.png", -1), 8, 1, 475, 225)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        movement(pygame.key.get_pressed())
        screen.fill((pygame.Color("White")))
        pygame.draw.line(screen, pygame.Color("Red"), (500, 20), (500, size[1] - 40), 4)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
