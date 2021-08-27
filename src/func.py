# coding:utf-8
# version 1
import pygame
import sys
import os
# import easygui
import random
import time
from pygame.locals import *
from sys import exit
from cell import *
import chess

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

#加载骰子图像
# dials = []
# for i in range(1, 7):
#     dials.append(pygame.image.load('images/dial' + str(i) + '.png'))


# 每格位置数组
a_map = [[311, 635], [273, 635], [231, 620], [213, 578], [213, 541], [235, 499], [198, 469], [156, 484], [
     118, 484], [76, 469], [61, 427], [61, 389], [61, 351], [61, 315], [61, 278], [76, 236], [118, 221], [
     156,221],[198,236], [235,206], [213,164], [213,127], [231,85], [273,70], [311,70], [349,70],[
    389,70], [427,70], [470,85], [485,126], [485,162], [470,206], [502,236], [543,221], [582,221],[
    622,236], [637,278], [637,315], [637,351], [637,389], [637,427], [623,469], [583,484], [543,484],[
    502,469], [470,499], [485,541], [485,578], [470,620], [427,635], [389,635], [349,635]]

#起点坐标
chicken_start=[[63,72],[123,72],[63,130],[123,130]]
hippo_start=[[578,72],[635,72],[578,130],[635,130]]
parrot_start=[[577,575],[637,575],[577,633],[637,633]]
duck_start=[[64,575],[123,575],[64,635],[123,635]]

#外围cell实例化
cell_map = [] # 地图中外围每个cell都实例化，放到一个list中
for i in range(len(a_map)):

    position = a_map[i]
    jump_po = []
    fly_po = []
    color = ""
    a_cell = cell(position, jump_po, fly_po, color)
    cell_map.append(a_cell)

for i in range(len(cell_map)):
    if i == 48:
        cell_map[i].jump_po = cell_map[0]
    elif i == 49:
        cell_map[i].jump_po = cell_map[1]
    elif i == 50:
        cell_map[i].jump_po = cell_map[2]
    elif i == 51:
        cell_map[i].jump_po = cell_map[3]
    else:
        cell_map[i].jump_po = cell_map[i+4]

    if i in [0,4,8,12,16,20,24,28,32,36,40,44,48]:#黄色
        cell_map[i].color = "yellow"
    elif i in [1,5,9,13,17,21,25,29,33,37,41,45,49]:#蓝色
        cell_map[i].color = "blue"
    elif i in [2,6,10,14,18,22,26,30,34,38,42,46,50]:#红色
        cell_map[i].color = "red"
    else:#绿色
        cell_map[i].color = "green"

    if i == 6:
        cell_map[i].fly_po = cell_map[18]
    elif i==19:
        cell_map[i].fly_po = cell_map[31]
    elif i == 32:
        cell_map[i].fly_po = cell_map[44]
    elif i== 45:
        cell_map[i].fly_po = cell_map[5]
    else:
        cell_map[i].fly_po = []

#终点cell实例化
chicken_end=[]
hippo_end=[]
parrot_end=[]
duck_end=[]
for c in [[118,351],[156,351],[194,351],[233,351],[271,351],[315,351]]:
    newcell= cell(c,None,None,'yellow')
    chicken_end.append(newcell)
for h in [[349,125],[349,161],[349,199],[349,237],[349,275],[349,317]]:
    newcell= cell(h,None,None,'blue')
    hippo_end.append(newcell)
for p in [[582,351],[543,351],[504,351],[466,351],[428,351],[383,351]]:
    newcell= cell(p,None,None,'red')
    parrot_end.append(newcell)
for d in [[349,579],[349,542],[349,504],[349,467],[349,428],[349,384]]:
    newcell= cell(d,None,None,'green')
    duck_end.append(newcell)


# chicken_map = a_map[16:] + a_map[:13] + [[118,351],[156,351],[194,351],[233,351],[271,351],[315,351]]
# hippo_map = a_map[29:] + a_map[:26] + [[349,125],[349,161],[349,199],[349,237],[349,275],[349,317]]
# parrot_map = a_map[-10:] + a_map[:-13] + [[582,351],[543,351],[504,351],[466,351],[428,351],[383,351]]
# duck_map = a_map[3:] + [[349,579],[349,542],[349,504],[349,467],[349,428],[349,384]]
chicken_map = cell_map[16:] + cell_map[:13] + chicken_end
hippo_map = cell_map[29:] + cell_map[:26] + hippo_end
parrot_map = cell_map[-10:] + cell_map[:-13] + parrot_end
duck_map = cell_map[3:] + duck_end

#获取不同棋子的地图
def getMap():
    return chicken_map,hippo_map,parrot_map,duck_map

# 写文字方法
# def fillText(text, position):
#     TextFont = pygame.font.Font('images/font1.ttf', 40)
#     newText = TextFont.render('分数:'+str(text), True, (0, 0, 0))
#     canvas.blit(newText, position)

# 画玩家方法
def drawPlayer(name, po):
    if name == 'chick':
        canvas.blit(chicken, chicken_map[po].position)
    if name == 'hippo':
        canvas.blit(hippo, hippo_map[po].position)
    if name == 'parrot':
        canvas.blit(parrot, parrot_map[po].position)
    if name == 'duck':
        canvas.blit(duck, duck_map[po].position)
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

# 画出对应步数的骰子
# def drawDial(step, position):
    # canvas.blit(dials[step-1], position)
    # pass

def chosenChess(step,color):
    return []
