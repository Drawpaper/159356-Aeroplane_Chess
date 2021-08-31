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
    def checkJump(self,chess):
        if self.jump_po!=[]:
            chess.cur_cell.position=self.jump_po
            chess.sum+=4
            self.cur_chess.append(chess)
            return chess
        else:
            return None
    def checkFly(self,chess):
        if self.fly_po!=[]:
            chess.cur_cell.position=self.fly_po
            chess.sum+=12
            self.cur_chess.append(chess)
            return chess
        else:
            return None
    def checkCollide(self):
        pass
