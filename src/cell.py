class cell:
    def __init__(self, position, jump_po, fly_po, color):
        self.position = position
        #跳棋的cell,不能跳棋为[]
        self.jump_po = jump_po
        #飞棋后的cell，不能飞棋为[]
        self.fly_po = fly_po
        self.color = color
        self.cur_chess = []
    def addChess(self,chess):
        self.cur_chess.append(chess)
    def deleteCurrentChess(self,chess):
        self.cur_chess.remove(chess)
    def checkJump(self):
        pass
    def checkFly(self):
        pass
    def checkCollide(self):
        pass
