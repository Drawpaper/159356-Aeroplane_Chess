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
from func import getMap
from func import drawDial
from func import getOptions
from func import selectOption
from func import determineOption
from func import getAirport
from chess import *
from cell import *

pygame.init()
# 窗口定位
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)
# 设置一个长宽窗口
canvas = pygame.display.set_mode((967, 741))
canvas.fill([255, 255, 255])
# 设置窗口标题
pygame.display.set_caption("Game")

# 图片加载
start = pygame.image.load('images/start.png')
start = pygame.transform.scale(start, (967, 741))
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

# 表示到达终点
final = 0
# 创建游戏控制

#实例化十六个棋子
chicken_map,hippo_map,parrot_map,duck_map = getMap()
chicken_airport,hippo_airport,parrot_airport,duck_airport=getAirport()
#黄色
chicken_chess = [chess('chick',i+1, chicken_airport) for i in range(4)] #第1，2，3，4个棋子
for i in range(4):
    chicken_chess[i].cur_cell=chicken_airport[i]
#蓝色
hippo_chess = [chess('hippo',i+1, hippo_airport) for i in range(4)]
for i in range(4):
    hippo_chess[i].cur_cell=hippo_airport[i]
#红色
parrot_chess = [chess('parrot',i+1, parrot_airport) for i in range(4)]
for i in range(4):
    parrot_chess[i].cur_cell=parrot_airport[i]
#绿色
duck_chess = [chess('duck',i+1, duck_airport) for i in range(4)]
for i in range(4):
    duck_chess[i].cur_cell=duck_airport[i]

#后来需要去掉，现在这样可以让程序运行起来，之后要使用每个chess中的sum
sum_1 = 0
sum_2 = 0
sum_3 = 0
sum_4 = 0

def gameControl():
    global turn,sum_1,sum_2,sum_3,sum_4

    step = random.randint(1, 6)#得到随机扔色子数
    # step = 1

    if state == 'START':
        canvas.blit(start, (0, 0))
    elif state == 'READY':
        canvas.blit(bg, (0, 0))
        startpoint()
    elif state == 'RUNNING':
        canvas.blit(bg, (0, 0))
        startpoint()
        if turn == 0:
            #随机摇骰子->判断骰子点数->判断当前可选骰子->玩家选择棋子->判断当前棋子位置->计算棋子前进位置：起飞、跳、飞
            #希纯：

            # ① 一个函数以step(1-6的随机数/掷色子的结果)为输入，找到对应的骰子图像显示在屏幕上（需要把页面变宽 能够放下一个筛子的图像）
            drawDial(step)

            #一个函数以step与当前轮棋子的类为输入，判断骰子点数选择可选棋子 返回可选棋子的类（注意若step数大于其到达终点的格数此棋子不可选）（多个）
            # ② options=getOptions(2,'chick',chicken_chess) ！！！cur_cell未解决！！！ 具体解释见func.py

            #一个函数以可选棋子的类为输入，在其中触发弹框使用户选择移动的棋子，返回对应棋子的类（一个）
            # ③ selectOption(options,chicken_chess) ！！！cur_cell未解决！！！ 具体解释见func.py
            options=getOptions(step,'chick',chicken_chess)
            num=int(selectOption(options,chicken_chess))
            cur_sum=determineOption(step,num,chicken_chess)
            # chessNow=chicken_chess[num-1]
            # if chessNow.sum==None:
            #     chessNow.sum=0
            #     chessNow.takeOff(num-1)
            #     for i in cell_map:
            #
            #     cell()
            #     # chessNow.update(chessNow.cur_cell)
            # else:
            #     chessNow.sum+=step
            #     chessNow.update(chessNow.cur_cell)
            #     checkJump(chessNow)
            #     checkFly(chessNow)
            #     # chessNow.update(chessNow.cur_cell)

            #莹莹：
            #一个函数以用户所选棋子的类为输入，判断棋子的位置（通过判断棋子的sum或cur_cell）
                #若为none则为起始点，则执行chess中的起飞函数。该函数使当前棋子移动到该棋子路线上的第一个cell，并更新此cell的信息
                #若不为none则为普通点，则根据调用当前棋子的地图与sum判断前进后的cell，返回该cell
                    #调用该cell中的checkJump与checkFly函数。这两个函数以当前chess为输入判断是否该chess是否可以跳棋或飞棋若能返回最终cell，不能返回None
                    #根据得到的最终位置的cell更新当前chess中的sum与cur_cell信息,并更新最终cell与之前cell中cur_chess的信息
            #将下面的drawPlayer(chicken, sum_1)替换为
            # for i in range(len(chicken_chess)):
            #     drawPlayer(chicken_chess[i].chess_type, chicken_chess[i].sum)
            #其他同理，即可通过运行程序验证程序是否正确

            #这部分之后可以去掉
            sum_1 = sum_1 + cur_sum
        #    drawPlayer(chicken, sum_1)
        elif turn == 1:
            drawDial(step)
            options=getOptions(step,'hippo',hippo_chess)
            num=int(selectOption(options,hippo_chess))
            cur_sum=determineOption(step,num,hippo_chess)
            sum_2 = sum_2 + cur_sum
         #   drawPlayer(hippo, sum_2)
        elif turn == 2:
            drawDial(step)
            options=getOptions(step,'parrot',parrot_chess)
            num=int(selectOption(options,parrot_chess))
            cur_sum=determineOption(step,num,parrot_chess)
            sum_3 = sum_3 + cur_sum
         #   drawPlayer(parrot, sum_3)
        elif turn == 3:
            drawDial(step)
            options=getOptions(step,'duck',duck_chess)
            num=int(selectOption(options,duck_chess))
            cur_sum=determineOption(step,num,duck_chess)
            sum_4 = sum_4 + cur_sum
        #    drawPlayer(duck, sum_4)
            # if sum_4 < 60:
            #     pass
            # else:
            #     # canvas.blit(gameover, (40, 340))
            #     final = 1

        #此部分做替换
        drawPlayer(chicken, sum_1)
        drawPlayer(hippo, sum_2)
        drawPlayer(parrot, sum_3)
        drawPlayer(duck, sum_4)

    elif state == 'END':
        canvas.blit(end, (0, 0))

#画原始的4枚棋子
def startpoint():
    for i in range(1,5):
        if chicken_chess[i-1].sum == None:
            drawStartPoints(chicken_chess[i-1].chess_type,-i)
        else:
            continue
    for i in range(1,5):
        if hippo_chess[i-1].sum == None:
            drawStartPoints(hippo_chess[i-1].chess_type,-i)
        else:
            continue
    for i in range(1,5):
        if duck_chess[i-1].sum == None:
            drawStartPoints(duck_chess[i-1].chess_type,-i)
        else:
            continue
    for i in range(1,5):
        if parrot_chess[i-1].sum == None:
            drawStartPoints(parrot_chess[i-1].chess_type,-i)
        else:
            continue

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
                state = 'RUNNING'
        elif event.type == KEYDOWN and event.key == K_0 and turn == 0:
            gameControl()
            turn = 1
        elif event.type == KEYDOWN and event.key == K_1 and turn == 1:
            gameControl()
            turn = 2
        elif event.type == KEYDOWN and event.key == K_2 and turn == 2:
            gameControl()
            turn = 3
        elif event.type == KEYDOWN and event.key == K_3 and turn == 3:
            gameControl()
            turn = 0
        elif final == 1:
            pygame.time.delay(15)
            pygame.display.update()
            state = 'END'
            gameControl()
    pygame.display.update()
