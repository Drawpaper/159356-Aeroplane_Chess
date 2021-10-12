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
# import eventlet
import copy

import tkinter as tk
from  tkinter import messagebox

pygame.init()
# 窗口定位
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 30)
# 设置一个长宽窗口
canvas = pygame.display.set_mode((967, 741))
canvas.fill([255, 255, 255])
# 设置窗口标题
pygame.display.set_caption("飞行棋")

col = 20
row = 30
# 图片加载
# start = pygame.image.load('images/start.png')
# bg = pygame.image.load('images/bg.png')
# end = pygame.image.load('images/gameover.png')
#
# chicken = pygame.image.load('images/chick.png')
# chicken = pygame.transform.scale(chicken, (37, 37))
# chicken_square = pygame.image.load('images/chick_square.png') # 迭子图片
# chicken_square= pygame.transform.scale(chicken_square, (37, 37))
#
# duck = pygame.image.load('images/duck.png')
# duck = pygame.transform.scale(duck, (37, 37))
# duck_square = pygame.image.load('images/duck_square.png') # 迭子图片
# duck_square = pygame.transform.scale(duck_square, (37, 37))
#
# hippo = pygame.image.load('images/hippo.png')
# hippo = pygame.transform.scale(hippo, (37, 37))
# hippo_square = pygame.image.load('images/hippo_square.png') # 迭子图片
# hippo_square = pygame.transform.scale(hippo_square, (37, 37))
#
# parrot = pygame.image.load('images/parrot.png')
# parrot = pygame.transform.scale(parrot, (37, 37))
# parrot_square = pygame.image.load('images/parrot_square.png') # 迭子图片
# parrot_square = pygame.transform.scale(parrot_square, (37, 37))

# 每格位置数组
a_map = [[311, 635], [273, 635], [231, 620], [213, 578], [213, 541], [235, 499], [198, 469], [156, 484], [
     118, 484], [76, 469], [61, 427], [61, 389], [61, 351], [61, 315], [61, 278], [76, 236], [118, 221], [
     156,221],[198,236], [235,206], [213,164], [213,127], [231,85], [273,70], [311,70], [349,70],[
    389,70], [427,70], [470,85], [485,126], [485,162], [470,206], [502,236], [543,221], [582,221],[
    622,236], [637,278], [637,315], [637,351], [637,389], [637,427], [623,469], [583,484], [543,484],[
    502,469], [470,499], [485,541], [485,578], [470,620], [427,635], [389,635], [349,635]]

# 起点坐标
chicken_start=[[63,72],[123,72],[63,130],[123,130]]
hippo_start=[[578,72],[635,72],[578,130],[635,130]]
parrot_start=[[577,575],[637,575],[577,633],[637,633]]
duck_start=[[64,575],[123,575],[64,635],[123,635]]
# 起点坐标实例化（飞机场内cell）
chicken_airport=[]
hippo_airport=[]
parrot_airport=[]
duck_airport=[]
for c in chicken_start:
    newcell= cell(c,None,None,'yellow')
    chicken_airport.append(newcell)
for h in hippo_start:
    newcell= cell(h,None,None,'blue')
    hippo_airport.append(newcell)
for p in parrot_start:
    newcell= cell(p,None,None,'red')
    parrot_airport.append(newcell)
for d in duck_start:
    newcell= cell(d,None,None,'green')
    duck_airport.append(newcell)



# 外围cell实例化
cell_map = [] # 地图中外围每个cell都实例化，放到一个list中
for i in range(len(a_map)):
    position = a_map[i]
    jump_po = []
    fly_po = []
    color = ""
    a_cell = cell(position, jump_po, fly_po, color)
    a_cell.cur_chess = []
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

# 终点cell实例化
chicken_end=[]
hippo_end=[]
parrot_end=[]
duck_end=[]
chicken_end_pos=[[118,351],[156,351],[194,351],[233,351],[271,351],[315,351]]
hippo_end_pos=[[349,125],[349,161],[349,199],[349,237],[349,275],[349,317]]
parrot_end_pos=[[582,351],[543,351],[504,351],[466,351],[428,351],[383,351]]
duck_end_pos=[[349,579],[349,542],[349,504],[349,467],[349,428],[349,384]]
for c in chicken_end_pos:
    newcell= cell(c,[],[],'yellow')
    chicken_end.append(newcell)
for h in hippo_end_pos:
    newcell= cell(h,[],[],'blue')
    hippo_end.append(newcell)
for p in parrot_end_pos:
    newcell= cell(p,[],[],'red')
    parrot_end.append(newcell)
for d in duck_end_pos:
    newcell= cell(d,[],[],'green')
    duck_end.append(newcell)


# 不同棋子各自的外围+终点路线
chicken_map_pos = a_map[16:] + a_map[:13] + chicken_end_pos
hippo_map_pos = a_map[29:] + a_map[:26] + hippo_end_pos
parrot_map_pos = a_map[-10:] + a_map[:-13] + parrot_end_pos
duck_map_pos = a_map[3:] + duck_end_pos
#每个棋子有55个格子
chicken_map = cell_map[16:] + cell_map[:13] + chicken_end
hippo_map = cell_map[29:] + cell_map[:26] + hippo_end
parrot_map = cell_map[-10:] + cell_map[:-13] + parrot_end
duck_map = cell_map[3:] + duck_end

# 获取不同棋子的地图
def getMap():
    return chicken_map,hippo_map,parrot_map,duck_map
def getMappos():
    return chicken_map_pos,hippo_map_pos,parrot_map_pos,duck_map_pos

# 获取不同棋子的起点cell，即飞机场内cell
def getAirport():
    return chicken_airport,hippo_airport,parrot_airport,duck_airport

# 写文字方法
# def fillText(text, position):
#     TextFont = pygame.font.Font('images/font1.ttf', 40)
#     newText = TextFont.render('分数:'+str(text), True, (0, 0, 0))
#     canvas.blit(newText, position)

# 画玩家方法
# def drawPlayer(name, po):
#     if name == 'chick':
#         if len(chicken_map[po].cur_chess)>1:# 若当前cell有迭子情况（有多个同种类型棋子），则画chicken_square.png
#             canvas.blit(chicken_square, tuple(chicken_map[po].position))
#         else:
#             canvas.blit(chicken, tuple(chicken_map[po].position))
#
#     if name == 'hippo':
#         if len(hippo_map[po].cur_chess)>1:
#             canvas.blit(hippo_square, tuple(hippo_map[po].position))
#         else:
#             canvas.blit(hippo, tuple(hippo_map[po].position))
#
#     if name == 'parrot':
#         if len(parrot_map[po].cur_chess)>1:
#             canvas.blit(parrot_square, tuple(parrot_map[po].position))
#         else:
#             canvas.blit(parrot, tuple(parrot_map[po].position))
#
#     if name == 'duck':
#         if len(duck_map[po].cur_chess)>1:
#             canvas.blit(duck_square, tuple(duck_map[po].position))
#         else:
#             canvas.blit(duck, tuple(duck_map[po].position))
#     pygame.display.update()
#
# #画起点方法
# def drawStartPoints(name, po):
#     if name == 'chick':
#         canvas.blit(chicken, chicken_start[po])
#     if name == 'hippo':
#         canvas.blit(hippo, hippo_start[po])
#     if name == 'parrot':
#         canvas.blit(parrot, parrot_start[po])
#     if name == 'duck':
#         canvas.blit(duck, duck_start[po])
#     pygame.display.update()



# 加载骰子图像
dials = []
# for i in range(1, 7):
#     dials.append(pygame.image.load('images/'+str(i) + '.png'))
# 以step(1-6的随机数/掷色子的结果)为输入，找到对应的骰子图像显示在屏幕上（需要把页面变宽 能够放下一个筛子的图像）
def drawDial(step):
    canvas.blit(dials[step-1], [737,0])


# 1.输入：①step，②当前轮棋子的类别,③该类棋子list
# 2.根据骰子点数选择可选棋子
#   ①如果掷色子数step为6，增加飞机场的棋子起飞这一选择
#   ②判断在地图上已出发的棋子有几个，是否在step步后未超出终点，若未超出则作为选择之一，若step数大于其到达终点的格数此棋子不可选
# 3.返回：可选棋子的chess_num，即该棋子在该类棋子list中的（index+1）（多个options）
# e.g.  getOptions(2,'chick',chicken_chess)
# 增添条件: step数之内的cell（不包括最终的cell）若有cell有 [两个或两个以上] 的 [其他颜色] 的相同颜色棋子（叠子）则当前棋子也不能被选择
def getOptions(step,chesstype,chesslist):
    if chesstype=='chick':
        chessmap=chicken_map_pos
        map=chicken_map
    elif chesstype=='hippo':
        chessmap=hippo_map_pos
        map=hippo_map
    elif chesstype=='parrot':
        chessmap=parrot_map_pos
        map=parrot_map
    else:
        chessmap=duck_map_pos
        map=duck_map

    options=[]
    for a_piece in chesslist:
        pos=a_piece.cur_cell.position # 得到当前棋子所在cell的位置坐标

        if pos not in chessmap: # 该棋子还未起飞
            if  step==6: # 掷色子数为6，满足起飞的条件
                options.append(a_piece.chess_num)
        else:
            index=chessmap.index(pos)
            if (index+step+1) > len(chessmap): # 若step数大于其到达终点的格数，此棋子不可选
                pass
            else:
                pass_num=0
                for s in range(1,step+1):
                    checked_cell=map[index+s]
                    if len(checked_cell.cur_chess)>1 and checked_cell.cur_chess[0].chess_type!=chesstype: #step数内的cell中，无敌方迭子
                        pass
                    else:
                        pass_num=pass_num+1

                if  pass_num==step:
                    options.append(a_piece.chess_num)
    return options



# 1.输入:①可选棋子的chess_num，即该棋子在该类棋子list中的（index+1）,为getOptions函数的返回值
#       ②当前轮棋子的类别
#       ③该类棋子list
# 2.触发弹框使用户选择最终移动的棋子
# 3.返回：棋子的chess_num，
#       (num-1)即为该棋子在chicken_chess或其他种chesslist中的index，
#       chicken_chess[num-1]即为所选的棋子
# selectOption([1,2],chicken_chess) options中的数字不可能为0
def selectOption(options,chesslist):

    root = tk.Tk()
    root.title("Choose a piece")
    root.geometry('500x200')

    if options==[]:# 没有棋子可以移动
        messagebox.showinfo("warning","In this turn, you have no pieces to move.")
        root.quit()
        root.destroy()
        return False

    chesstype=chesslist[0].chess_type
    if chesstype=='chick':
        chessmap=chicken_map_pos
    elif chesstype=='hippo':
        chessmap=hippo_map_pos
    elif chesstype=='parrot':
        chessmap=parrot_map_pos
    else:
        chessmap=duck_map_pos

    options_text="" # 显示所有可选择的棋子信息
    for op in options:
        pos=chesslist[op-1].cur_cell.position # 该棋子当前位置的坐标
        if pos not in chessmap: # 还未起飞的棋子
            options_text=options_text+"No"+str(op)+": At the airport! "+"\n"
        else:
            index=chessmap.index(pos) # 在该类棋子的路线中，该坐标是第几个位置 ----> 使玩家知道是地图上哪个棋子
            options_text=options_text+"No"+str(op)+": on the "+str(index)+"th grid of its own route"+str(pos)+"\n"

    la = tk.Label(root, text= options_text)
    la.pack()
    xls_text = tk.StringVar()
    xls = tk.Entry(root, textvariable = xls_text)
    xls_text.set("")
    xls.pack()

    def on_click(): # 点击press触发
        global num
        num = xls_text.get()
        if num=="" or (int(num) not in options): # 若玩家未输入所选棋子的号码 或 输入不符合规则的数字，新弹出警告窗口
            messagebox.showinfo("warning","You must choose a piece and enter its number!")
        if num!="" and (int(num) in options): # 若玩家输入符合规则的所选棋子的号码，原窗口自动关闭
            root.quit()
            root.destroy()

    tk.Button(root, text="press", command = on_click).pack()
    root.mainloop()
    return num

#AI
#没有选择时，pass （options=[]）
#只有一个选择时，就选这个 （len（options）==1）
#选择有两个以上 (len（options）>1)
     #因为只有掷到6才能起飞，机会难得，优先级最高，凡是掷到6都执行起飞操作
     #当棋子移动时，为避免其它棋子优先到达终点，撞子操作要优于跳子和飞子
     #普通棋子移动，以移动步数大小作为优先标准
def ai(step,options,chesslist):
    if options==[]:
        return False
    else:
        # global num
        num=options[0]
        if len(options)>1:
            steps=Simulated_moving(step,num,chesslist)
            for x in range(1,len(options)):
                steps1=Simulated_moving(step,options[x],chesslist)
                if steps1>=steps:
                    num=options[x]
                    steps=steps1
    return num

#模拟ai移动
def Simulated_moving(step,num,chesslist):
    if num==False:
        return 0
    else:
        #用来记录执行了哪些函数:起飞+100,优先级最高；碰撞+50，第二优先；移动+step，跳+4，飞+12，优先级按总的移动步数
        funcs=0
        chesslist1=copy.deepcopy(chesslist)
        chickmap=copy.deepcopy(chicken_map)
        hippomap=copy.deepcopy(hippo_map)
        parrotmap=copy.deepcopy(parrot_map)
        duckmap=copy.deepcopy(duck_map)
        # for x in chesslist:
        #     chesslist1.append(x)
        # for x in chicken_map:
        #     chickmap.append(x)
        # for x in hippo_map:
        #     hippomap.append(x)
        # for x in parrot_map:
        #     parrotmap.append(x)
        # for x in duck_map:
        #     duckmap.append(x)
        chessNow=chesslist1[num-1]
        if chessNow.sum==None:
            chessNow.takeOff(num-1)
            c=chesslist1[num-1].cur_cell
            c.deleteCurrentChess(chessNow)
            funcs+=100

            #更新cell的信息
            if chessNow.chess_type=='chick':
                chessNow.cur_cell=chickmap[0]
                chickmap[0].cur_chess.append(chessNow)
            elif chessNow.chess_type=='hippo':
                chessNow.cur_cell=hippomap[0]
                hippomap[0].cur_chess.append(chessNow)
            elif chessNow.chess_type=='parrot':
                chessNow.cur_cell=parrotmap[0]
                parrotmap[0].cur_chess.append(chessNow)
            else:
                chessNow.cur_cell=duckmap[0]
                duckmap[0].cur_chess.append(chessNow)
            C=Simulated_collide(chessNow)
            if C==True:
                funcs+=50

        else:
            chessNow.sum+=step
            funcs+=step
            if chessNow.chess_type=='chick':
                chessmap=chickmap
            elif chessNow.chess_type=='hippo':
                chessmap=hippomap
            elif chessNow.chess_type=='parrot':
                chessmap=parrotmap
            else:
                chessmap=duckmap

            for i in range(len(chessmap)):
                if chessNow.cur_cell==chessmap[i]:
                    chessNow.cur_cell.deleteCurrentChess(chessNow)
                    chessNow.cur_cell=chessmap[i+step]
                    chessmap[i+step].cur_chess.append(chessNow)
                    break
            C=Simulated_collide(chessNow)
            if C==True:
                funcs+=50
            #飞棋
            flychess=chessNow.cur_cell.checkFly(chessNow)
            if flychess!=None:
                chessNow=flychess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+12]
                        chessmap[i+12].cur_chess.append(chessNow)
                        funcs+=12
                        break
                C=Simulated_collide(chessNow)
                if C==True:
                    funcs+=50

            #跳棋
            jumpchess=chessNow.cur_cell.checkJump(chessNow)
            if jumpchess!=None:
                chessNow=jumpchess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+4]
                        chessmap[i+4].cur_chess.append(chessNow)
                        funcs+=4
                        break
                C=Simulated_collide(chessNow)
                if C==True:
                    funcs+=50

            #飞棋
            flychess=chessNow.cur_cell.checkFly(chessNow)
            if flychess!=None:
                chessNow=flychess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+12]
                        chessmap[i+12].cur_chess.append(chessNow)
                        funcs+=12
                        break
                C=Simulated_collide(chessNow)
                if C==True:
                    funcs+=50
        #
        # if chickmap!=chicken_map or hippomap!=hippo_map or parrotmap!=parrot_map or duckmap!=duck_map:
        #     print("yes")
        # else:
        #     print("nooooo")
        return funcs

#模拟碰撞
def Simulated_collide(chess):
    chickairport=copy.deepcopy(chicken_airport)
    hippoairport=copy.deepcopy(hippo_airport)
    parrotairport=copy.deepcopy(parrot_airport)
    duckairport=copy.deepcopy(duck_airport)

    # for x in chicken_airport:
    #     chickairport.append(x)
    # for x in hippo_airport:
    #     hippoairport.append(x)
    # for x in parrot_airport:
    #     parrotairport.append(x)
    # for x in duck_airport:
    #     duckairport.append(x)

    c=chess.cur_cell
    collidechess=c.checkCollide(chess)
    if collidechess != None:
        for chess1 in collidechess:
            chess1.sum = None
            c.cur_chess.remove(chess1)
            if chess1.chess_type=='chick':
                for x in chickairport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            elif chess1.chess_type=='hippo':
                for x in hippoairport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            elif chess1.chess_type=='parrot':
                for x in parrotairport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            else:
                for x in duckairport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
        return True
    return False

#一个函数以用户所选棋子的类为输入，判断棋子的位置（通过判断棋子的sum或cur_cell）
    #若为none则为起始点，则执行chess中的起飞函数。该函数使当前棋子移动到该棋子路线上的第一个cell，并更新此cell的信息
    #若不为none则为普通点，则根据调用当前棋子的地图与sum判断前进后的cell，返回该cell

        #调用该cell中的checkCollide函数判断是否有与当前棋子颜色不同的其他棋子在此cell中
            #若有则返回这些棋子（注意：可能会有多个相同颜色的棋子在一个cell中），并将这些棋子的类初始化（置于起飞点）
            #若无则返回none

        #调用该cell中的checkJump与checkFly函数。这两个函数以当前chess为输入判断是否该chess是否可以跳棋或飞棋若能返回最终cell，不能返回None
        #根据得到的最终位置的cell更新当前chess中的sum与cur_cell信息,并更新最终cell与之前cell中cur_chess的信息

def determineOption(step,num,chesslist):
    if num==False:
        return 0
    else:
        chessNow=chesslist[num-1]
        if chessNow.sum==None:
            chessNow.takeOff(num-1)
            c=chesslist[num-1].cur_cell
            c.deleteCurrentChess(chessNow)
            #更新cell的信息
            if chessNow.chess_type=='chick':
                chessNow.cur_cell=chicken_map[0]
                chicken_map[0].cur_chess.append(chessNow)
            elif chessNow.chess_type=='hippo':
                chessNow.cur_cell=hippo_map[0]
                hippo_map[0].cur_chess.append(chessNow)
            elif chessNow.chess_type=='parrot':
                chessNow.cur_cell=parrot_map[0]
                parrot_map[0].cur_chess.append(chessNow)
            else:
                chessNow.cur_cell=duck_map[0]
                duck_map[0].cur_chess.append(chessNow)
            collide(chessNow)

        else:
            chessNow.sum+=step
            if chessNow.chess_type=='chick':
                chessmap=chicken_map
            elif chessNow.chess_type=='hippo':
                chessmap=hippo_map
            elif chessNow.chess_type=='parrot':
                chessmap=parrot_map
            else:
                chessmap=duck_map

            for i in range(len(chessmap)):
                if chessNow.cur_cell==chessmap[i]:
                    chessNow.cur_cell.deleteCurrentChess(chessNow)
                    chessNow.cur_cell=chessmap[i+step]
                    chessmap[i+step].cur_chess.append(chessNow)
                    break
            collide(chessNow)
            #飞棋
            flychess=chessNow.cur_cell.checkFly(chessNow)
            if flychess!=None:
                chessNow=flychess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+12]
                        chessmap[i+12].cur_chess.append(chessNow)
                        break
                collide(chessNow)

            #跳棋
            jumpchess=chessNow.cur_cell.checkJump(chessNow)
            if jumpchess!=None:
                chessNow=jumpchess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+4]
                        chessmap[i+4].cur_chess.append(chessNow)
                        break
                collide(chessNow)

            #飞棋
            flychess=chessNow.cur_cell.checkFly(chessNow)
            if flychess!=None:
                chessNow=flychess
                for i in range(len(chessmap)):
                    if chessNow.cur_cell==chessmap[i]:
                        chessNow.cur_cell.deleteCurrentChess(chessNow)
                        chessNow.cur_cell=chessmap[i+12]
                        chessmap[i+12].cur_chess.append(chessNow)
                        break
                collide(chessNow)

        return chessNow.sum

#撞子,将其他棋子初始化
def collide(chess):
    c=chess.cur_cell
    collidechess=c.checkCollide(chess)
    if collidechess != None:
        for chess1 in collidechess:
            chess1.sum = None
            c.cur_chess.remove(chess1)
            if chess1.chess_type=='chick':
                for x in chicken_airport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            elif chess1.chess_type=='hippo':
                for x in hippo_airport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            elif chess1.chess_type=='parrot':
                for x in parrot_airport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break
            else:
                for x in duck_airport:
                    if x.cur_chess==[]:
                        chess1.cur_cell=x
                        x.cur_chess.append(chess1)
                        break

def chosenChess(step,color):
    return []


# 输入：当前轮棋子的类别;该类棋子list
# 判断4个棋子是否全部都到达最后几个格子，若全部到达，出现弹框显示赢家，并返回1；否则，无弹框，返回0。
def findWinner(chesstype,chesslist):

    if chesstype=='chick':
        endmap=chicken_end_pos
    elif chesstype=='hippo':
        endmap=hippo_end_pos
    elif chesstype=='parrot':
        endmap=parrot_end_pos
    else:
        endmap=duck_end_pos

    end_num=0
    for c in chesslist:
        p=c.cur_cell.position
        if p in endmap: # 到达最后几个格子
            end_num=end_num+1

    if end_num == 4: # 4个棋子全部都到达最后几个格子
        root = tk.Tk()
        root.title(" W I N N E R ")
        root.geometry('500x200')
        winner=chesstype
        messagebox.showinfo(" congratulations ", winner+" are the winner !!!!! ")
        root.quit()
        root.destroy()
        return 1
    else:
        return 0
