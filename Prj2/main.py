import os
import pygame
import random
import sys
import datetime

pygame.init()
size = width, height = 1000, 500
screen_rect = (0, 0, width, height)
speed = 4
GRAVITY = 5
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Аэрохоккей')
clock = pygame.time.Clock()
FPS = 60


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["АЭРОХОККЕЙ", "",
                  "Правила игры:",
                  "Нужно забить шайбу в ворота противника",
                  "Игра идёт до тех пор, пока один из игроков не получит 5 очков "]

    fon = pygame.transform.scale(load_image('bg.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 25
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def final_screen(bita1_win, bita2_win):
    final_text = ["             КОНЕЦ", "",
                  "", "",
                  "       ПОЗДРАВЛЯЮ", "",
                  "Подсчёт результатов:", "",
                  f"КРАСНАЯ БИТА: {str(bita1_win)}", "",
                  f"СИНЯЯ БИТА: {str(bita2_win)}"]
    if bita1_win == 5:
        final_text[2] = "ПОБЕДИЛА КРАСНАЯ БИТА"
        color = "red"
    elif bita2_win == 5:
        final_text[2] = "ПОБЕДИЛА СИНЯЯ БИТА"
        color = "blue"
    else:
        final_text[2] = "   НИКТО НЕ ВЫИГРАЛ"
        final_text[4] = ""
        color = "black"
    fon = pygame.transform.scale(load_image('bg.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 35)
    text_coord = 40
    write_score(final_text)
    for line in final_text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 340
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


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


def make_text(bita1, bita2):
    text = [str(bita1), str(bita2)]
    text_coord = 420
    font_score = pygame.font.Font(None, 30)
    for line in text:
        string_rendered = font_score.render(line, 1, pygame.Color('black'))
        score_rect = string_rendered.get_rect()
        text_coord += 50
        score_rect.top = 40
        score_rect.x = text_coord
        screen.blit(string_rendered, score_rect)


def write_score(result):
    today = datetime.datetime.today().strftime("%d-%m-%Y-%H:%M:%S")
    with open('score.txt', 'a', encoding="UTF-8") as score_result:
        score_result.write(today + '\n')
        score_result.write(result[2].strip() + '\n')
        for i in range(8, 11, 2):
            score_result.write(result[i] + '\n')
        score_result.write('\n')


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
        self.puck_speed = [-8, 7, -6, -5, 5, 6, 7, 8]

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
            if self.rect.x > 500:
                if ((bita2.rect.x - self.rect.x > 0 and self.vx > 0) or
                        (bita2.rect.x - self.rect.x < 0 and self.vx < 0) or
                        (bita2.rect.y - self.rect.y == 0)):
                    self.vx = -self.vx
                elif ((bita2.rect.x - self.rect.x > 0 > self.vx) or
                        (bita2.rect.x - self.rect.x < 0 < self.vx) or
                        (bita2.rect.x - self.rect.x == 0)):
                    self.vy = -self.vy
            if self.rect.x < 500:
                if ((bita1.rect.x - self.rect.x < 0 and self.vx < 0) or
                        (bita1.rect.x - self.rect.x > 0 and self.vx > 0) or
                        (bita1.rect.y - self.rect.y == 0)):
                    self.vx = -self.vx
                elif ((bita1.rect.x - self.rect.x < 0 < self.vx) or
                        (bita1.rect.x - self.rect.x > 0 > self.vx) or
                        (bita1.rect.x - self.rect.x == 0)):
                    self.vy = -self.vy

        if self.rect.left < 0 or self.rect.left > 1000:
            self.kill()
            self.flag = 0
            bita1.rect.x = 100
            bita1.rect.y = 220
            bita2.rect.x = 850
            bita2.rect.y = 220


class Score(AnimatedPuck):
    def __init__(self, ap):
        self.rect = ap.rect

    def condition(self):
        if self.rect.left >= 1000 or self.rect.left <= 0:
            return True
        return False


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

radius = 30

bita1_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
pygame.draw.circle(bita1_image, pygame.Color("Red"), (radius, radius), radius)
bita1 = pygame.sprite.Sprite(bits)
bita1.image = bita1_image
bita1.rect = bita1.image.get_rect()
bita1.rect.x = 100
bita1.rect.y = 220
bita1_score = 0

bita2_image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
pygame.draw.circle(bita2_image, pygame.Color("Blue"), (radius, radius), radius)
bita2 = pygame.sprite.Sprite(bits)
bita2.image = bita2_image
bita2.rect = bita2.image.get_rect()
bita2.rect.x = 850
bita2.rect.y = 220
bita2_score = 0
all_sprites.add(bits)

height_vert_bord = random.randint(20, 100)
Border(40, 20, size[0] - 80, 10)
Border(40, size[1] - 40, size[0] - 80, 10)
Border(40, 20, 10, height_vert_bord)
Border(40, 370 + (100 - height_vert_bord), 10, height_vert_bord)
Border(size[0] - 40, 20, 10, height_vert_bord)
Border(size[0] - 40, 370 + (100 - height_vert_bord), 10, height_vert_bord)

ap = AnimatedPuck(load_image("circle_der.png", -1), 8, 1, 471, 220)
start_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    movement(pygame.key.get_pressed())
    screen.fill((pygame.Color("White")))
    sc = Score(ap)
    if sc.rect.left >= 1000:
        bita1_score += 1
    elif sc.rect.left <= 0:
        bita2_score += 1
    if bita1_score == 5 or bita2_score == 5:
        running = False
    make_text(bita1_score, bita2_score)
    if sc.condition():
        ap = AnimatedPuck(load_image("circle_der.png", -1), 8, 1, 471, 220)
        sc = Score(ap)
    all_sprites.update()
    pygame.draw.line(screen, pygame.Color("Red"), (500, 20), (500, size[1] - 40), 4)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

final_screen(bita1_score, bita2_score)
