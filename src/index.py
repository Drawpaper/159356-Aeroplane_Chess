# coding:utf-8
# version 1
import pygame
import sys
import os
import random
import time
from pygame.locals import *
from sys import exit

from func import drawPlayer
from func import drawStartPoints
pygame.init()
# 窗口定位
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)
# 设置一个长宽窗口
canvas = pygame.display.set_mode((737, 741))
canvas.fill([255, 255, 255])
# 设置窗口标题
pygame.display.set_caption("Game")

# 图片加载
start = pygame.image.load('images/start.png')
start = pygame.transform.scale(start, (750, 1000))
bg = pygame.image.load('images/bg.png')
end = pygame.image.load('images/gameover.png')

chicken = 'chick'
hippo = 'hippo'
parrot = 'parrot'
duck = 'duck'
# 设定游戏状态和玩家分数
state = 'START'
score_s = 0
score_p = 0
# 判断哪位玩家移动
turn = 0
# 控制玩家到达位置
sum_1 = 0
sum_2 = 0
sum_3 = 0
sum_4 = 0
# 控制玩家移动步数
step_1 = 0
step_2 = 0
step_3 = 0
step_4 = 0
# 表示到达终点
final = 0
# 创建游戏控制


def gameControl():
    global step_1, step_2, step_3, step_4, final, sum_1, sum_2, sum_3, sum_4, turn
    # step_s = random.randint(1, 4)
    # step_p = random.randint(1, 4)
    step_1 = 1
    step_2 = 1
    step_3 = 1
    step_4 = 1
    if state == 'START':
        canvas.blit(start, (0, 0))
    elif state == 'READY':
        canvas.blit(bg, (0, 0))
        drawPlayer(chicken, sum_1)
        drawPlayer(hippo, sum_2)
        drawPlayer(parrot, sum_3)
        drawPlayer(duck, sum_4)
    elif state == 'RUNNING':
        canvas.blit(bg, (0, 0))
        if turn == 0:
            sum_1 = sum_1 + step_1
            if sum_1 < 60:
                pass
            else:
                # canvas.blit(gameover, (40, 340))
                final = 1
        elif turn == 1:
            sum_2 = sum_2 + step_2
            if sum_2 < 60:
                pass
            else:
                # canvas.blit(gameover, (40, 340))
                final = 1
        elif turn == 2:
            sum_3 = sum_3 + step_3
            if sum_3 < 60:
                pass
            else:
                # canvas.blit(gameover, (40, 340))
                final = 1
        elif turn == 3:
            sum_4 = sum_4 + step_4
            if sum_4 < 60:
                pass
            else:
                # canvas.blit(gameover, (40, 340))
                final = 1
        drawPlayer(chicken, sum_1)
        drawPlayer(hippo, sum_2)
        drawPlayer(parrot, sum_3)
        drawPlayer(duck, sum_4)
    elif state == 'END':
        canvas.blit(end, (0, 0))

#画原始的4枚棋子
def startpoint():
    for i in range(1,5):
        drawStartPoints(chicken,-i)
    for i in range(1,5):
        drawStartPoints(hippo,-i)
    for i in range(1,5):
        drawStartPoints(duck,-i)
    for i in range(1,5):
        drawStartPoints(parrot,-i)

gameControl()
# 根据用户的操作切换游戏状态
while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            if state == 'START':
                state = 'READY'
                gameControl()
            if state == 'READY':
                startpoint()
                state = 'RUNNING'
        elif event.type == KEYDOWN and event.key == K_0 and turn == 0:
            gameControl()
            startpoint()
            turn = 1
        elif event.type == KEYDOWN and event.key == K_1 and turn == 1:
            gameControl()
            startpoint()
            turn = 2
        elif event.type == KEYDOWN and event.key == K_2 and turn == 2:
            gameControl()
            startpoint()
            turn = 3
        elif event.type == KEYDOWN and event.key == K_3 and turn == 3:
            gameControl()
            startpoint()
            turn = 0
        elif final == 1:
            pygame.time.delay(15)
            pygame.display.update()
            state = 'END'
            gameControl()
    pygame.display.update()
