from operator import attrgetter
import pygame as py
from pygame import mixer
from PIL import Image, ImageOps
import math
import random
import time
py.init()
# Folder Name and Screen
f_Images, f_made, f_Sounds = 'Images', 'made', 'Sounds'

screen_width, screen_height = 800, 600
screen = py.display.set_mode((screen_width, screen_height))
py.display.set_caption('Stickman Shooting Endless')

# Player
playerImg = py.image.load(f'{f_Images}/stand.svg')

# Huge Ball
huge_ballImg = py.image.load(f'{f_Images}/huge_ball.svg')

# Jars
JarsType = ['jar-a', 'jar-b']

JarImg, JarImg_mirror = [], []

for num in JarsType:
    img = Image.open(f'{f_Images}/{num}.png')
    img_resized = img.resize((95, 100))
    img_resized.save(f'{f_Images}/{f_made}/{num}_resized.png', quality = 90)

    img_mirror = ImageOps.mirror(img_resized)
    img_mirror.save(f'{f_Images}/{f_made}/{num}_mirror.png', quality = 90)

    JarImg.append(py.image.load(f'{f_Images}/{f_made}/{num}_resized.png'))
    JarImg_mirror.append(py.image.load(f'{f_Images}/{f_made}/{num}_mirror.png'))

class Jar:
    def __init__(self):
        if playerX > screen_width / 2:
            self.JarX = -95 / 2
        else:
            self.JarX = screen_width + 95 / 2
        self.JarY = random.randint(0, screen_height)

    def jar_move(self, x, y):
        divide_change = cal_distans(playerX - x, playerY - y) / 7

        self.JarX += (playerX - x) / divide_change
        self.JarY += (playerY - y) / divide_change

    def jar(self, x, y):
        if fever:
            num = 1
        else:
            num = 0

        if x < playerX:
            to_draw = JarImg[num]
        else:
            to_draw = JarImg_mirror[num]

        screen.blit(to_draw, (x - 95 / 2, y - 100 / 2))

    def jar_end(self, x, y, N):
        if huge_ball_state == 'shoot':
            distans = cal_distans(huge_ballX - x, huge_ballY - y)
            if distans < 169 / 2:
                global all_clean_time, all_clean_type, obtain, num

                mixer.Sound(f'{f_Sounds}/meow.wav').play()

                if fever:
                    inc = 8
                else:
                    inc = 1

                obtain += inc
                Jarnum.pop(N)
                if len(Jarnum) == 0:
                    if all_clean_type == 0:

                        # Fucking Nest
                        all_clean_time = t
                        obtain += 100
                elif len(Jarnum) == 1:
                    if abs(Jarnum[0].JarX - screen_width / 2) > screen_width / 2:

                        # Fucking Nest #2
                        all_clean_time = t
                        all_clean_type = 1
                        obtain += 100
                    else:
                        all_clean_type = 0

                num -= 1

    def player_end(self, x, y):
        distans = cal_distans(playerX - x, playerY - y)
        if distans < 50:
            global game_over, running

            game_over = True
            running = False

# Function
def player(x, y):
    screen.blit(playerImg, (x - 35 / 2, y - 99 / 2))

def shoot_huge_ball(x, y):
    global huge_ball_state
    if huge_ball_state == 'ready':

        global huge_ballX_change, huge_ballY_change

        divide_change = cal_distans(lastX_change, lastY_change) / 24

        huge_ballX_change = lastX_change / divide_change
        huge_ballY_change = lastY_change / divide_change

    huge_ball_state = 'shoot'
    screen.blit(huge_ballImg, (x - 169 / 2, y - 169 / 2))

def cal_distans(x, y):
    return math.sqrt((x ** 2) + (y ** 2))

def write_letter(size, letter, color, pos):
    if size == 'large' or size == 'small':
        if size == 'large':
            font_size = 64
        else:
            font_size = 32

        font = py.font.SysFont(None, font_size)
        score = font.render(letter, True, color)
        if "score:" in letter:
            global letter_width
            letter_width = score.get_size()[0]

        screen.blit(score, pos)

# Game Loop Endless
running = True
while running:

    # Initialization
        # Player
    playerX, playerY = screen_width / 2, 480
    playerX_change, playerY_change, lastX_change, lastY_change = 0, 0, 1, 0

        # Huge Ball
    huge_ballX, huge_ballY = 0, 0
    huge_ball_state = 'ready'

        # Jars
    Jarnum = []

        # Others
    all_clean_time = -9999
    all_clean_type = 0
    game_over = False
    lastk_space = True
    t = 0
    obtain = 0

    # Main Game Loop
    while running:
        time.sleep(0.03)
        t += 1

        fever = (0 <= t - all_clean_time <= 130)

        screen.fill((150, 150, 150))

        # Operation
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

            if event.type == py.KEYDOWN:
                keys = event.key

                if keys == py.K_ESCAPE:
                    running = False
                if keys == py.K_LEFT or keys == py.K_a:
                    playerX_change, lastX_change = -1, -1
                if keys == py.K_RIGHT or keys == py.K_d:
                    playerX_change, lastX_change = 1, 1
                if keys == py.K_UP or keys == py.K_w:
                    playerY_change, lastY_change = -1, -1
                if keys == py.K_DOWN or keys == py.K_s:
                    playerY_change, lastY_change = 1, 1

            if event.type == py.KEYUP:
                keys = event.key

                if ((keys == py.K_LEFT or keys == py.K_a) and playerX_change < 0) or\
                    ((keys == py.K_RIGHT or keys == py.K_d) and playerX_change > 0):

                    playerX_change = 0
                if ((keys == py.K_UP or keys == py.K_w) and playerY_change < 0) or\
                    ((keys == py.K_DOWN or keys == py.K_s) and playerY_change > 0):

                    playerY_change = 0

        keys = py.key.get_pressed()
        if not(keys[py.K_LEFT] or keys[py.K_RIGHT] or keys[py.K_a] or keys[py.K_d]):
            if lastY_change != 0:
                lastX_change = 0

        if not(keys[py.K_UP] or keys[py.K_DOWN] or keys[py.K_w] or keys[py.K_s]):
            if lastX_change != 0:
                lastY_change = 0

        if keys[py.K_SPACE] and not lastk_space:
            if huge_ball_state == 'ready':
                huge_ballX, huge_ballY = playerX, playerY
                shoot_huge_ball(huge_ballX, huge_ballY)
                mixer.Sound(f'{f_Sounds}/pop.wav').play()

        lastk_space = keys[py.K_SPACE]

        # Player
        divide_change = cal_distans(playerX_change, playerY_change) / 10

        if divide_change > 0:
            playerX += playerX_change / divide_change
            playerY += playerY_change / divide_change
        if playerX <= 35 / 2:
            playerX = 35 / 2
        elif playerX >= screen_width - 35 / 2:
            playerX = screen_width - 35 / 2
        if playerY <= 99 / 2:
            playerY = 99 / 2
        elif playerY >= screen_height - 99 / 2:
            playerY = screen_height - 99 / 2

        # Huge Ball Movement
        if huge_ballX <= -169 / 2 or huge_ballX >= screen_width + 169 / 2 or\
            huge_ballY <= -169 / 2 or huge_ballY >= screen_height + 169 / 2:

            huge_ball_state = 'ready'

        if huge_ball_state == 'shoot':
            huge_ballX += huge_ballX_change
            huge_ballY += huge_ballY_change
            shoot_huge_ball(huge_ballX, huge_ballY)

        # Jars
        if t % 10 == 0:
            Jarnum.append(Jar())

        Jarnum.sort(key = attrgetter('JarY'))

        num = 0
        while num < len(Jarnum):
            Jarnum[num].jar_move(Jarnum[num].JarX, Jarnum[num].JarY)
            Jarnum[num].jar(Jarnum[num].JarX, Jarnum[num].JarY)
            Jarnum[num].player_end(Jarnum[num].JarX, Jarnum[num].JarY)
            Jarnum[num].jar_end(Jarnum[num].JarX, Jarnum[num].JarY, num)

            num += 1

        # Update Display
        player(playerX, playerY)

        if fever:
            write_letter('large', "All Clear!", (255, 215, 0), (290, 350))

            exagge = 'large'
        else:
            exagge = 'small'

        write_letter(exagge, "score:" + str(obtain), (235, 20, 110), (20, 50))

        py.display.update()

    # After Game Over
    if game_over:
        write_letter('small', f"survival time:{round(t * 3 / 100, 1)} s",\
                     (56, 30, 254), (27 + letter_width, 50))

        write_letter('large', "Game Over", (70, 12, 187), (100, 400))
        write_letter('small', "Press Space to Retry", (70, 12, 187), (100, 450))

        mixer.Sound(f'{f_Sounds}/Dun_Dun_Dunnn.wav').play()
        py.display.update()
        running = True
        t = 0

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    running = False

        time.sleep(0.03)
        t += 1

        if t >= 30:
            keys = py.key.get_pressed()
            if keys[py.K_SPACE]:
                break