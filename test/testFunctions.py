import unittest
import sys
sys.path.append('../src/images/')
sys.path.append('../src/')

from test1 import collide
from test1 import get_Airport_Chess
from test1 import determineOption
from cell import *
from chess import *

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
        self.chicken_chess = [chess('chick',i+1, self.chessmap) for i in range(5)] #第1，2，3,4个棋子
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
    def test_collide_1(self):#chess2被初始化
        a,b,c,d=get_Airport_Chess()
        b[0].cur_chess=[]
        chess1=self.chicken_chess[0]
        chess2=chess('hippo',6, self.chessmap)
        chess2.sum=0
        chess2.cur_cell=self.chessmap[0]
        self.chessmap[0].cur_chess.append(chess2)
        collide(chess1)
        self.assertEqual(chess2.sum,None,msg="test_collide_1 was failed.")
        self.assertEqual(chess2.cur_cell,[],msg="test_collide_1 was failed.")
    def test_collide_2(self):#颜色相同，不会碰撞 初始化
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
        chess1=self.chicken_chess[0]
        chess1.sum=0
        determineOption(1,1,self.chicken_chess)
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

if __name__ == '__main__':
    unittest.main()
