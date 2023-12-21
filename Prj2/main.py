import os
import pygame

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
bita1.rect.x = 100
bita1.rect.y = 190

Border(40, 20, size[0] - 80, 10)
Border(40, size[1] - 40, size[0] - 80, 10)
Border(40, 20, 10, 140)
Border(40, 330, 10, 140)
Border(size[0] - 40, 20, 10, 140)
Border(size[0] - 40, 330, 10, 140)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            bita1.rect.top += speed
        elif key[pygame.K_UP]:
            bita1.rect.top -= speed
        elif key[pygame.K_LEFT]:
            bita1.rect.left -= speed
        elif key[pygame.K_RIGHT]:
            bita1.rect.left += speed
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()
