# coding:utf-8
# version 1
import pygame
import sys
import os
import easygui
import random
import time
from pygame.locals import *
from sys import exit
pygame.init()
# 窗口定位
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)
# 设置一个长宽窗口
canvas = pygame.display.set_mode((737, 741))
canvas.fill([255, 255, 255])
# 设置窗口标题
pygame.display.set_caption("飞行棋")

col = 20
row = 30
# 图片加载
start = pygame.image.load('images/start.png')
bg = pygame.image.load('images/bg.png')
end = pygame.image.load('images/gameover.png')
chicken = pygame.image.load('images/chick.png')
chicken = pygame.transform.scale(chicken, (37, 37))
duck = pygame.image.load('images/duck.png')
duck = pygame.transform.scale(duck, (37, 37))
hippo = pygame.image.load('images/hippo.png')
hippo = pygame.transform.scale(hippo, (37, 37))
parrot = pygame.image.load('images/parrot.png')
parrot = pygame.transform.scale(parrot, (37, 37))

#骰子图像
# dials = []
# for i in range(0, 4):
#     dials.append(pygame.image.load('images/dial' + str(i) + '.png'))

class cell:
    def __init__(self, position, jump_po, fly_po, color):
        self.position = position
        self.jump_po = jump_po
        self.fly_po = fly_po
        self.color = color
    def checkJump(self):
        pass
    def checkFly(self):
        pass
    def checkCollide(self):
        pass

class chess:
    def __init__(self, cur_po, chess_type, chess_num):
        self.cur_po = cur_po
        self.chess_type = chess_type
        self.chess_num = chess_num

# 每格位置数组
a_map = [[311, 635], [273, 635], [231, 620], [213, 578], [213, 541], [235, 499], [198, 469], [156, 484], [
     118, 484], [76, 469], [61, 427], [61, 389], [61, 351], [61, 315], [61, 278], [76, 236], [118, 221], [
     156,221],[198,236], [235,206], [213,164], [213,127], [231,85], [273,70], [311,70], [349,70],[
    389,70], [427,70], [470,85], [485,126], [485,162], [470,206], [502,236], [543,221], [582,221],[
    622,236], [637,278], [637,315], [637,351], [637,389], [637,427], [623,469], [583,484], [543,484],[
    502,469], [470,499], [485,541], [485,578], [470,620], [427,635], [389,635], [349,635]]

chicken_map = a_map[16:] + a_map[:13] + [[118,351],[156,351],[194,351],[233,351],[271,351],[315,351]]
hippo_map = a_map[29:] + a_map[:26] + [[349,125],[349,161],[349,199],[349,237],[349,275],[349,317]]
parrot_map = a_map[-10:] + a_map[:-13] + [[582,351],[543,351],[504,351],[466,351],[428,351],[383,351]]
duck_map = a_map[3:] + [[349,579],[349,542],[349,504],[349,467],[349,428],[349,384]]

#起点坐标
chicken_start=[[63,72],[123,72],[63,130],[123,130]]
hippo_start=[[578,72],[635,72],[578,130],[635,130]]
parrot_start=[[577,575],[637,575],[577,633],[637,633]]
duck_start=[[64,575],[123,575],[64,635],[123,635]]

# cell实例化
cell_map = [] #地图中每个cell都实例化，放到一个list中
# # 不同颜色的cell，分别放到不同的list中
# yellow_cells=[]
# blue_cells=[]
# red_cells=[]
# green=[]
for i in (0,len(a_map)-1):

    position = a_map[i]
    jump_po = []
    fly_po = []
    color = ""

    if i == 48:
        jump_po = a_map[0]
    elif i == 49:
        jump_po = a_map[1]
    elif i == 50:
        jump_po = a_map[2]
    elif i == 51:
        jump_po = a_map[3]
    else:
        jump_po = a_map[i+4]

    if i in [0,4,8,12,16,20,24,28,32,36,40,44,48]:#黄色
        color = "yellow"
    elif i in [1,5,9,13,17,21,25,29,33,37,41,45,49]:#蓝色
        color = "blue"
    elif i in [2,6,10,14,18,22,26,30,34,38,42,46,50]:#红色
        color = "red"
    else:#绿色
        color = "green"

    if i == 6:
        fly_po = a_map[18]
    elif i==19:
        fly_po = a_map[31]
    elif i == 32:
        fly_po = a_map[44]
    elif i== 45:
        fly_po = a_map[5]
    else:
        fly_po = []

    a_cell = cell(position, jump_po, fly_po, color)
    cell_map.append(a_cell)



# 写文字方法
# def fillText(text, position):
#     TextFont = pygame.font.Font('images/font1.ttf', 40)
#     newText = TextFont.render('分数:'+str(text), True, (0, 0, 0))
#     canvas.blit(newText, position)

# 画玩家方法
def drawPlayer(name, po):
    if name == 'chick':
        canvas.blit(chicken, chicken_map[po])
    if name == 'hippo':
        canvas.blit(hippo, hippo_map[po])
    if name == 'parrot':
        canvas.blit(parrot, parrot_map[po])
    if name == 'duck':
        canvas.blit(duck, duck_map[po])
    pygame.display.update()

#画起点方法
def drawStartPoints(name, po):
    if name == 'chick':
        canvas.blit(chicken, chicken_start[po])
    if name == 'hippo':
        canvas.blit(hippo, hippo_start[po])
    if name == 'parrot':
        canvas.blit(parrot, parrot_start[po])
    if name == 'duck':
        canvas.blit(duck, duck_start[po])
    pygame.display.update()

# 创建画出随机步数的方法
# def drawStep(step, position):
    # canvas.blit(dials[step-1], position)
    # pass
