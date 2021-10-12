import unittest
import sys
sys.path.append('../src/images/')
sys.path.append('../src/')

from src.test1 import collide
from src.test1 import determineOption
from src.test1 import getMap
from src.test1 import getAirport
from src.test1 import getOptions
from src.test1 import findWinner
from src.cell import *
from src.chess import *

class TestFunction(unittest.TestCase):
    def setUp(self):
        self.cell1=cell([311, 635],[213, 541],[61, 351],'yellow')
        self.cell2=cell([273, 635],[],[],'yellow')
        self.cell3=cell([231, 620],[198, 469],[61, 278],'blue')
        self.cell4=cell([213, 578],[156, 484],[],'yellow')
        self.cell5=cell([582,221],[],[485,578],'yellow')
        self.chessmap=[]
        self.chessmap.append(self.cell1)
        self.chessmap.append(self.cell2)
        self.chessmap.append(self.cell3)
        self.chessmap.append(self.cell4)
        self.chessmap.append(self.cell5)
        self.chicken_chess = [chess('chick',i+1, self.chessmap) for i in range(5)] #第1，2，3, 4个棋子
        for i in range(5):
            self.chicken_chess[i].cur_cell=self.chessmap[i]
            self.chessmap[i].cur_chess.append(self.chicken_chess[i])
        print('start.')

    def tearDown(self):
        print('end.')

    #测试takeOff
    def test_takeOff(self):
        chess1=chess('chick',6, self.chessmap)
        self.assertEqual(chess1.sum,None,msg="test_takeOff was failed.")
        chess1.takeOff(1)
        self.assertEqual(chess1.sum,0,msg="test_takeOff was failed.")
        self.assertEqual(chess1.cur_cell,self.chessmap[1],msg="test_takeOff was failed.")

    #测试checkJump
    def test_checkJump_1(self): #checkJump正常运行
        chess1=self.chicken_chess[0]
        chess1.sum=0
        chess1.cur_cell.checkJump(chess1)
        self.assertEqual(chess1.cur_cell.position,[213, 541],msg="test_checkJump_1 was failed.")
        self.assertEqual(chess1.sum,4,msg="test_checkJump_1 was failed.")
    def test_checkJump_2(self): #jump_po==[]
        chess1=self.chicken_chess[1]
        chess1.sum=0
        chess1.cur_cell.checkJump(chess1)
        self.assertEqual(chess1.cur_cell.position,[273, 635],msg="test_checkJump_2 was failed.")
        self.assertEqual(chess1.sum,0,msg="test_checkJump_2 was failed.")
    def test_checkJump_3(self): #颜色不一致
        chess1=self.chicken_chess[2]
        chess1.sum=0
        chess1.cur_cell.checkJump(chess1)
        self.assertNotEqual(chess1.cur_cell.position,[198, 469],msg="test_checkJump_3 was failed.")
        self.assertNotEqual(chess1.sum,4,msg="test_checkJump_3 was failed.")

    #测试checkFly
    def test_checkFly_1(self): #checkFly正常运行
        chess1=self.chicken_chess[0]
        chess1.sum=0
        chess1.cur_cell.checkFly(chess1)
        self.assertEqual(chess1.cur_cell.position,[61, 351],msg="test_checkFly_1 was failed.")
        self.assertEqual(chess1.sum,12,msg="test_checkFly_1 was failed.")
    def test_checkFly_2(self): #fly_po==[]
        chess1=self.chicken_chess[1]
        chess1.sum=0
        chess1.cur_cell.checkFly(chess1)
        self.assertEqual(chess1.cur_cell.position,[273, 635],msg="test_checkFly_2 was failed.")
        self.assertEqual(chess1.sum,0,msg="test_checkFly_2 was failed.")
    def test_checkFly_3(self): #颜色不一致
        chess1=self.chicken_chess[2]
        chess1.sum=0
        chess1.cur_cell.checkFly(chess1)
        self.assertNotEqual(chess1.cur_cell.position,[61, 278],msg="test_checkFly_3 was failed.")
        self.assertNotEqual(chess1.sum,12,msg="test_checkFly_3 was failed.")

    #测试checkCollide
    def test_checkCollide_1(self): #checkCollide正常运行
        chess1=self.chicken_chess[0]
        chess2=chess('hippo',6, self.chessmap)
        chess2.cur_cell=self.chessmap[0]
        self.chessmap[0].cur_chess.append(chess2)
        all_chess=self.cell1.checkCollide(chess1)
        self.assertIn(chess2,all_chess,msg="test_checkCollide_1 was failed.")
    def test_checkCollide_2(self): #相同颜色的棋子在一个格里，不会碰撞
        chess1=self.chicken_chess[0]
        chess2=chess('chick',6, self.chessmap)
        chess2.cur_cell=self.chessmap[0]
        self.chessmap[0].cur_chess.append(chess2)
        all_chess=self.cell1.checkCollide(chess1)
        self.assertIsNone(all_chess,msg="test_checkCollide_2 was failed.")
    def test_checkCollide_3(self): #格子里只有一个棋子
        chess1=self.chicken_chess[0]
        all_chess=self.cell1.checkCollide(chess1)
        self.assertIsNone(all_chess,msg="test_checkCollide_3 was failed.")

    #测试collide
    def test_collide(self):#颜色相同，不会碰撞 初始化
        chess1=self.chicken_chess[0]
        chess2=chess('chick',6, self.chessmap)
        chess2.sum=0
        chess2.cur_cell=self.chessmap[0]
        self.chessmap[0].cur_chess.append(chess2)
        collide(chess1)
        self.assertEqual(chess2.sum,0,msg="test_collide_2 was failed.")
        self.assertNotEqual(chess2.cur_cell,[],msg="test_collide_2 was failed.")

    #测试determineOption
    def test_determineOption_1(self): #起飞
        chess1=self.chicken_chess[0]
        determineOption(1,1,self.chicken_chess)
        self.assertEqual(chess1.sum,0,msg="test_determineOption_1 was failed.")
        self.assertNotEqual(chess1.cur_cell,self.cell1,msg="test_determineOption_1 was failed.")
    def test_determineOption_2(self): #跳一步
        chess1=self.chicken_chess[1]
        chess1.sum=0
        determineOption(1,2,self.chicken_chess)
        self.assertEqual(chess1.sum,1,msg="test_determineOption_2 was failed.")
        self.assertNotEqual(chess1.cur_cell,self.cell1,msg="test_determineOption_2 was failed.")
    def test_determineOption_3(self): #jump
        chess1=self.chicken_chess[3]
        chess1.sum=0
        determineOption(2,4,self.chicken_chess)
        self.assertEqual(chess1.sum,6,msg="test_determineOption_3 was failed.")
        self.assertNotEqual(chess1.cur_cell,self.cell1,msg="test_determineOption_3 was failed.")
    def test_determineOption_4(self): #fly
        chess1=self.chicken_chess[4]
        chess1.sum=0
        determineOption(1,5,self.chicken_chess)
        self.assertEqual(chess1.sum,13,msg="test_determineOption_4 was failed.")
        self.assertNotEqual(chess1.cur_cell,self.cell1,msg="test_determineOption_4 was failed.")


    # 测试以下三个要点：
    #   1.如果掷色子数step为6，增加飞机场的棋子起飞这一选择
    #   2.判断在地图上已出发的棋子有几个，是否在step步后未超出终点，若未超出则作为选择之一，若step数大于其到达终点的格数此棋子不可选
    #   3.step数之内的cell（不包括最终的cell）若有cell有 [两个或两个以上] 的 [其他颜色] 的相同颜色棋子（叠子）则当前棋子也不能被选择
    def test_getOptions(self):

        chicken_map,hippo_map,parrot_map,duck_map = getMap()
        chicken_airport,hippo_airport,parrot_airport,duck_airport=getAirport()

        chickchess1=chess('chick',1,chicken_map) # 起点
        chickchess1.cur_cell=chicken_airport[0]

        chickchess2=chess('chick',2,chicken_map) # 在倒数第四个cell
        chickchess2.cur_cell=chicken_map[-4]

        chickchess4=chess('chick',4,chicken_map) # 在倒数第二个cell
        chickchess4.cur_cell=chicken_map[-2]

        chickchess3=chess('chick',3,chicken_map) # 在第二个cell
        chickchess3.cur_cell=chicken_map[2]

        hippochess1=chess('hippo',1,hippo_map) # 两个hippo类型棋子，在chicken_map第三个cell的位置
        hippochess1.cur_cell=chicken_map[3]
        hippochess2=chess('hippo',2,hippo_map)
        hippochess2.cur_cell=chicken_map[3]
        chicken_map[3].cur_chess=[hippochess1,hippochess2] # 在chicken_map第三个cell的位置，hippo类型棋子 ----> 迭子

        chesslist=[chickchess1,chickchess2,chickchess3,chickchess4]

        # 预期结果：
        # 测试1：step=1 , chickenchess  [2,3,4]
        # 测试2：step=2 ，chickenchess  [2]
        # 测试3：step=3 , chickenchess  [2]
        # 测试4：step=4 , chickenchess  []
        # 测试5：step=5 ，chickenchess  []
        # 测试6：step=6 , chickenchess  [1]

        options1=getOptions(1,'chick',chesslist)# 测试1
        self.assertEqual(options1,[2,3,4])

        options2=getOptions(2,'chick',chesslist)# 测试2
        self.assertEqual(options2,[2])

        options3=getOptions(3,'chick',chesslist)# 测试3
        self.assertEqual(options3,[2])

        options4=getOptions(4,'chick',chesslist)# 测试4
        self.assertEqual(options4,[])

        options5=getOptions(5,'chick',chesslist)# 测试5
        self.assertEqual(options5,[])

        options6=getOptions(6,'chick',chesslist)# 测试6
        self.assertEqual(options6,[1])


    # chick是赢家，函数返回1
    def test_findWinner_1(self):
        chicken_map,hippo_map,parrot_map,duck_map = getMap()

        # chick棋子【全在】最后几个cell
        chickchess1=chess('chick',1,chicken_map) # 在倒数第1个cell
        chickchess1.cur_cell=chicken_map[-1]

        chickchess2=chess('chick',2,chicken_map) # 在倒数第2个cell
        chickchess2.cur_cell=chicken_map[-2]

        chickchess3=chess('chick',3,chicken_map) # 在倒数第3个cell
        chickchess3.cur_cell=chicken_map[-3]

        chickchess4=chess('chick',4,chicken_map) # 在倒数第4个cell
        chickchess4.cur_cell=chicken_map[-4]

        chesslist=[chickchess1,chickchess2,chickchess3,chickchess4]

        result=findWinner('chick',chesslist)
        self.assertEqual(result,1)


    # chick不是赢家，函数返回0
    def test_findWinner_0(self):
        chicken_map,hippo_map,parrot_map,duck_map = getMap()

        # chick棋子【不都在】最后几个cell
        chickchess1=chess('chick',1,chicken_map) # 在倒数第1个cell
        chickchess1.cur_cell=chicken_map[-1]

        chickchess2=chess('chick',2,chicken_map) # 在倒数第2个cell
        chickchess2.cur_cell=chicken_map[-2]

        chickchess3=chess('chick',3,chicken_map) # 在第3个cell
        chickchess3.cur_cell=chicken_map[3]

        chickchess4=chess('chick',4,chicken_map) # 在第4个cell
        chickchess4.cur_cell=chicken_map[4]

        chesslist=[chickchess1,chickchess2,chickchess3,chickchess4]

        result=findWinner('chick',chesslist)
        self.assertEqual(result,0)


if __name__ == '__main__':
    unittest.main()
