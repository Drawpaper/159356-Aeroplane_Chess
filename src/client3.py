import socket
import json
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
from func import getMappos
from func import drawDial
from func import getOptions
from func import selectOption
from func import determineOption
from func import getAirport
from func import findWinner
from func import ai
from chess import *
from cell import *

from login import login

import time
from threading import Thread

pygame.init()
# 窗口定位
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)
# 设置一个长宽窗口
canvas = pygame.display.set_mode((967, 741))
canvas.fill([255, 255, 255])
# 设置窗口标题
pygame.display.set_caption("Game3")

# 图片加载
start = pygame.image.load('images/start.png')
start = pygame.transform.scale(start, (967, 741))
bg = pygame.image.load('images/bg.png')
end = pygame.image.load('images/gameover.png')
# 图片加载2
chicken = pygame.image.load('images/chick.png')
chicken = pygame.transform.scale(chicken, (37, 37))
duck = pygame.image.load('images/duck.png')
duck = pygame.transform.scale(duck, (37, 37))
hippo = pygame.image.load('images/hippo.png')
hippo = pygame.transform.scale(hippo, (37, 37))
parrot = pygame.image.load('images/parrot.png')
parrot = pygame.transform.scale(parrot, (37, 37))

# chicken = 'chick'
# hippo = 'hippo'
# parrot = 'parrot'
# duck = 'duck'
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
    chicken_airport[i].cur_chess.append(chicken_chess[i])
#蓝色
hippo_chess = [chess('hippo',i+1, hippo_airport) for i in range(4)]
for i in range(4):
    hippo_chess[i].cur_cell=hippo_airport[i]
    hippo_airport[i].cur_chess.append(hippo_chess[i])
#红色
parrot_chess = [chess('parrot',i+1, parrot_airport) for i in range(4)]
for i in range(4):
    parrot_chess[i].cur_cell=parrot_airport[i]
    parrot_airport[i].cur_chess.append(parrot_chess[i])
#绿色
duck_chess = [chess('duck',i+1, duck_airport) for i in range(4)]
for i in range(4):
    duck_chess[i].cur_cell=duck_airport[i]
    duck_airport[i].cur_chess.append(duck_chess[i])

#后来需要去掉，现在这样可以让程序运行起来，之后要使用每个chess中的sum
sum_1 = 0
sum_2 = 0
sum_3 = 0
sum_4 = 0
chicken_map_pos,hippo_map_pos,parrot_map_pos,duck_map_pos=getMappos()

def drawAllchess():
    # 为了先显示色子数字再让玩家做出选择，使用pygame.display.update()，但这使得选择棋子时棋盘被清空，
    # 玩家无法看着棋盘中的棋子位置做出选择，所以将原在gameControl()中部分代码封装，在更新画面前将所有棋子画出

        for i in range(4):#len(chicken_chess)
            if chicken_chess[i].cur_cell.position in chicken_map_pos:
                drawPlayer(chicken_chess[i].chess_type, chicken_map_pos.index(chicken_chess[i].cur_cell.position))#.sum
            # else:
            #     canvas.blit(chicken,tuple(chicken_chess[i].cur_cell.position))

        for i in range(4):
            # if hippo_chess[i].sum!=None:
            if hippo_chess[i].cur_cell.position in hippo_map_pos:
                drawPlayer(hippo_chess[i].chess_type, hippo_map_pos.index(hippo_chess[i].cur_cell.position))
            # else:
            #     canvas.blit(hippo, tuple(hippo_chess[i].cur_cell.position))

        for i in range(4):
            if parrot_chess[i].cur_cell.position in parrot_map_pos:
                drawPlayer(parrot_chess[i].chess_type, parrot_map_pos.index(parrot_chess[i].cur_cell.position))
            # else:
            #     canvas.blit(parrot, tuple(parrot_chess[i].cur_cell.position))

        for i in range(4):
            if duck_chess[i].cur_cell.position in duck_map_pos:
                drawPlayer(duck_chess[i].chess_type, duck_map_pos.index(duck_chess[i].cur_cell.position))
            # else:
            #     canvas.blit(duck, tuple(duck_chess[i].cur_cell.position))


def gameControl(s,n):
    global turn,sum_1,sum_2,sum_3,sum_4,final

    step = s #得到随机扔色子数

    if state == 'START':
        canvas.blit(start, (0, 0))
    elif state == 'READY':
        canvas.blit(bg, (0, 0))
        startpoint()
    elif state == 'RUNNING':
        canvas.blit(bg, (0, 0))
        startpoint()

        drawDial(step)
        pygame.display.update()

        drawAllchess()
        pygame.display.update()
        time.sleep(0.16)
        if turn+1 == player_num:
            if turn == 0 :
                #随机摇骰子->判断骰子点数->判断当前可选骰子->玩家选择棋子->判断当前棋子位置->计算棋子前进位置：起飞、跳、飞
                #希纯：
                # ① 一个函数以step(1-6的随机数/掷色子的结果)为输入，找到对应的骰子图像显示在屏幕上（需要把页面变宽 能够放下一个筛子的图像）
                # drawDial(step)

                #一个函数以step与当前轮棋子的类为输入，判断骰子点数选择可选棋子 返回可选棋子的类（注意若step数大于其到达终点的格数此棋子不可选）（多个）
    ##################(修改)step数之内的cell（不包括最终的cell）若有cell有两个或两个以上的其他颜色的相同颜色棋子（叠子）则当前棋子也不能被选择【√】

                # ② options=getOptions(2,'chick',chicken_chess) ！！！cur_cell未解决！！！ 具体解释见func.py

                #一个函数以可选棋子的类为输入，在其中触发弹框使用户选择移动的棋子，返回对应棋子的类（一个）
                # ③ selectOption(options,chicken_chess) ！！！cur_cell未解决！！！ 具体解释见func.py
                options=getOptions(step,'chick',chicken_chess)
                num=int(selectOption(options,chicken_chess))
                cur_sum=determineOption(step,num,chicken_chess)
                AI=0
                final=findWinner('chick',chicken_chess)
                if final==1:
                    return

                #莹莹：
                #一个函数以用户所选棋子的类为输入，判断棋子的位置（通过判断棋子的sum或cur_cell）
                    #若为none则为起始点，则执行chess中的起飞函数。该函数使当前棋子移动到该棋子路线上的第一个cell，并更新此cell的信息
                    #若不为none则为普通点，则根据调用当前棋子的地图与sum判断前进后的cell，返回该cell
    #####################(修改，增加)调用该cell中的checkCollide函数判断是否有与当前棋子颜色不同的其他棋子在此cell中
                            #若有则返回这些棋子（注意：可能会有多个相同颜色的棋子在一个cell中），并将这些棋子的类初始化（置于起飞点）
                            #若无则返回none
                        #调用该cell中的checkJump与checkFly函数。这两个函数以当前chess为输入判断是否该chess是否可以跳棋或飞棋若能返回最终cell，不能返回None
    #########################(修改，增加)若可以跳棋或飞棋则仍需再次调用cell中的checkCollide函数判断是否有与当前棋子颜色不同的其他棋子在最终cell中
                                #若有则返回这些棋子（注意：可能会有多个相同颜色的棋子在一个cell中），并将这些棋子的类初始化（置于起飞点）
                                #若无则返回none
                        #根据得到的最终位置的cell更新当前chess中的sum与cur_cell信息,并更新最终cell与之前cell中cur_chess的信息

                #希纯：
    #############（修改，增加）判断当前类别所有棋子的位置，若分别位于最后的几个格子内则将final置1，弹框显示‘xxx色的玩家获胜’【√】


            #另外需要希纯修改的：
                #每次需要先让用户看到本轮骰子再显示弹框让用户选择  【√】
                #将叠子棋子用方形图片代替，图片已经上传在image文件夹里（稍有些难需要考虑一下）【√】

            elif turn == 1:
                options=getOptions(step,'hippo',hippo_chess)
                num=int(selectOption(options,hippo_chess))
                cur_sum=determineOption(step,num,hippo_chess)
                AI=0
                final=findWinner('hippo',hippo_chess)
                if final==1:
                    return
            elif turn == 2:
                options=getOptions(step,'parrot',parrot_chess)
                num=int(selectOption(options,parrot_chess))
                cur_sum=determineOption(step,num,parrot_chess)
                AI=1
                final=findWinner('parrot',parrot_chess)
                if final==1:
                    return
            elif turn == 3:
                options=getOptions(step,'duck',duck_chess)
                num=int(ai(step,options,duck_chess))
                cur_sum=determineOption(step,num,duck_chess)
                AI=0
                final=findWinner('duck',duck_chess)
                if final==1:
                    return

                # if sum_4 < 60:
                #     pass
                # else:
                #     # canvas.blit(gameover, (40, 340))
                #     final = 1
            canvas.blit(bg, (0, 0))
            startpoint()
            drawAllchess()
            return num
        else:
            if turn == 0:
                options=getOptions(step,'chick',chicken_chess)
                cur_sum=determineOption(step,n,chicken_chess)
                AI=0
                final=findWinner('chick',chicken_chess)
                if final==1:
                    return
            elif turn == 1:
                options=getOptions(step,'hippo',hippo_chess)
                cur_sum=determineOption(step,n,hippo_chess)
                AI=0
                final=findWinner('hippo',hippo_chess)
                if final==1:
                    return
            elif turn == 2:
                options=getOptions(step,'parrot',parrot_chess)
                cur_sum=determineOption(step,n,parrot_chess)
                AI=1
                final=findWinner('parrot',parrot_chess)
                if final==1:
                    return
            elif turn == 3:
                options=getOptions(step,'duck',duck_chess)
                cur_sum=determineOption(step,n,duck_chess)
                AI=0
                final=findWinner('duck',duck_chess)
                if final==1:
                    return
            canvas.blit(bg, (0, 0))
            startpoint()
            drawAllchess()
    elif state == 'END':
        canvas.blit(end, (0, 0))

    pygame.display.update()

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

gameControl(random.randint(1, 6),None)
# 根据用户的操作切换游戏状态
s = socket.socket()
s.connect(('127.0.0.1', 6666))
player_num = None
cur_num = None
data = {
            'protocol': 'connect',
            'username': 'user1',
            'password': '111111'
        }

s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
AI=0
bytes = eval(s.recv(4096).decode('utf8').split('|#|')[0])
s.settimeout(0.1)
while True:

    try:
        bytes = eval(s.recv(4096).decode('utf8').split('|#|')[0])
        print(bytes)
    except socket.timeout:
        pass
    if bytes:
        if player_num == None and bytes['protocol'] == 'connect':
            player_num = bytes['number']
            print(bytes)

            # log in
            users= {'user1':'111111','user2':'222222','user3':'333333','user4':'444444'}
            users=login(bytes,users)
            # print(users)

            bytes = None
        elif bytes['protocol'] == 'ready':
            if state == 'START':
                state = 'READY'
                gameControl(random.randint(1, 6),None)
            if state == 'READY':
                state = 'RUNNING'
            bytes = None
        elif bytes['protocol'] =='running' :
            turn = bytes['cur_number']
            select_chess = bytes['move_chess']
            step = bytes['step']
            final = bytes['if_final']
            # AI=bytes['AI']
            gameControl(step,select_chess)
            if turn == 3 :
                turn = 0
                AI=0
            elif turn==2:
                turn=3
                AI=1
            else:
                turn += 1
                AI=0
            bytes = None

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif final == 1:
            pygame.time.delay(15)
            pygame.display.update()
            state = 'END'
            gameControl(random.randint(1, 6),None)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and player_num == 1:
            if state == 'START':
                state = 'READY'
                gameControl(random.randint(1, 6),None)
                data = {
                    'protocol':'ready'
                }
                s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
            if state == 'READY':
                state = 'RUNNING'
            print(103)
        elif event.type == KEYDOWN and event.key == K_0 and turn == 0 and turn +1 == player_num:
            turnWindow=tk.Tk()
            turnWindow.title('Turn')
            tk.messagebox.showinfo(title = 'Hint',message = "It is your turn~~~ ")
            turnWindow.quit()
            turnWindow.destroy()

            step = random.randint(1, 6)
            move_chess = gameControl(step,None)
            data = {
                'protocol':'running',
                'cur_number':turn,
                'move_chess':move_chess,
                'step':step,
                'if_final':final
                # 'AI':AI
            }
            s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
            turn = 1
            AI=0
        elif event.type == KEYDOWN and event.key == K_1 and turn == 1 and turn +1 == player_num:
            turnWindow=tk.Tk()
            turnWindow.title('Turn')
            tk.messagebox.showinfo(title = 'Hint',message = "It is your turn~~~ ")
            turnWindow.quit()
            turnWindow.destroy()

            step = random.randint(1, 6)
            move_chess = gameControl(step,None)
            data = {
                'protocol':'running',
                'cur_number':turn,
                'move_chess':move_chess,
                'step':step,
                'if_final':final
                # 'AI':AI
            }
            s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
            turn = 2
            AI=0
        elif event.type == KEYDOWN and event.key == K_2 and turn == 2 and turn +1 == player_num:
            turnWindow=tk.Tk()
            turnWindow.title('Turn')
            tk.messagebox.showinfo(title = 'Hint',message = "It is your turn~~~ ")
            turnWindow.quit()
            turnWindow.destroy()

            step = random.randint(1, 6)
            move_chess = gameControl(step,None)
            data = {
                'protocol':'running',
                'cur_number':turn,
                'move_chess':move_chess,
                'step':step,
                'if_final':final
                # 'AI':AI
            }
            s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
            turn = 3
            AI=1
        elif AI==1 and turn == 3 and turn +1 == player_num:
            step = random.randint(1, 6)
            move_chess = gameControl(step,None)
            data = {
                'protocol':'running',
                'cur_number':turn,
                'move_chess':move_chess,
                'step':step,
                'if_final':final
                # 'AI':AI
            }
            s.sendall((json.dumps(data, ensure_ascii=False) + '|#|').encode())
            turn = 0
            AI=0
    pygame.display.update()
