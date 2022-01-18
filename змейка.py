import pygame
import random
import os
import sys

pygame.init()

# цвет карты и счёта

white = (255, 255, 255)
black = (0, 0, 0)

# цвет еды

red = (255, 0, 0)

# цвет змейки и текста

green = (0, 100, 0)
yellow = (192, 255, 0)
violet = (238, 130, 238)
fuchsia = (255, 0, 255)
mediumOrchid = (186, 85, 211)
mediumPurple = (147, 112, 219)
purple = (128, 0, 128)
indigo = (75, 0, 130)
slateBlue = (106, 90, 205)
mediumSlateBlue = (123, 104, 238)
lightSteelBlue = (176, 196, 222)
darkTurquoise = (0, 206, 209)
aquamarine = (127, 255, 212)
mediumVioletRed = (199, 21, 133)
hotPink = (255, 105, 180)
paleVioletRed = (219, 112, 147)
lightCoral = (240, 128, 128)
salmon = (250, 128, 114)
darkSeaGreen = (143, 188, 143)
lightSkyBlue = (176, 226, 255)
lightGreen = (144, 238, 144)
maroon = (255, 52, 179)

# добавление цветов в список для использования метода random

colors = [maroon, lightGreen, lightSkyBlue, darkSeaGreen, salmon, lightCoral, paleVioletRed, hotPink, mediumVioletRed,
          aquamarine, darkTurquoise, lightSteelBlue, mediumSlateBlue, slateBlue, indigo, purple, mediumPurple,
          mediumOrchid, fuchsia, violet]

# задаются размеры игрового поля

width = 600
height = 400
FPS = 50

dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

# счёт, отображающий количество набранных очков

font_style = pygame.font.SysFont('times', 25)
score_font = pygame.font.SysFont('times', 35)


def score(score):
    value = score_font.render("Счёт: " + str(score), True, black)
    dis.blit(value, [0, 0])


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# зарисовка квадратов, составляющих змейку
# цвет змейки определяется методом random


def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, random.choice(colors), [x[0], x[1], snake_block, snake_block])

# функции, обображающие сообщения в случае проигрыша


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 3, height / 4])


def message1(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 2])


def message2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 3, height * 4 / 7])


# главный экран (меню)

def start_screen():
    intro_text = ["Змейка"
                  ]

    # добавление картинки в качестве фона

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    dis.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        dis.blit(string_rendered, intro_rect)

        # цикл главного меню

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


start_screen()


# цикл игры

def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length = 1

    # добавление еды

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(white)
            message("Вы проиграли!", red)
            message1("Чтобы начать заново нажмите 'Пробел',", red)
            message2("чтобы выйти 'esc'", red)
            score(Length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()

        # возможность играть с помощью клавиш-стрелок (вверх, вниз, вправо, влево)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        snake_Head = []

        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake(snake_block, snake_List)
        score(Length - 1)

        pygame.display.update()

        # если змейка съедает еду, прибавляется ещё одно звено

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()