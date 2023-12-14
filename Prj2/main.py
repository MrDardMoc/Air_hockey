import os
import pygame


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


def my_pole(screen, size):
    pygame.draw.circle(screen, (255, 255, 255), (1000 // 2, 500 // 2), 15)
    pygame.draw.rect(screen, pygame.Color("Red"), (20, 20, size[0] - 40, 10))
    pygame.draw.rect(screen, pygame.Color("Red"), (20, size[1] - 40, size[0] - 40, 10))
    pygame.draw.rect(screen, pygame.Color("Red"), (20, 20, 10, 140))
    pygame.draw.rect(screen, pygame.Color("Red"), (20, 330, 10, 140))
    pygame.draw.rect(screen, pygame.Color("Red"), (size[0] - 20, 20, 10, 140))
    pygame.draw.rect(screen, pygame.Color("Red"), (size[0] - 20, 330, 10, 140))


def main():
    pygame.init()
    size = 1000, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Аэрохоккей')
    all_sprites = pygame.sprite.Group()

    bita1_image = load_image('test.png')
    bita1 = pygame.sprite.Sprite(all_sprites)
    bita1.image = bita1_image
    bita1.rect = bita1.image.get_rect()
    bita1.rect.x = 100
    bita1.rect.y = 150
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        my_pole(screen, size)
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
