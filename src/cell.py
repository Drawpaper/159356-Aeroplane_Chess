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
        if self.jump_po!=[] and ((self.color=='yellow' and chess.chess_type=='chick') or (self.color=='blue' and chess.chess_type=='hippo') or (self.color=='red' and chess.chess_type=='parrot') or (self.color=='green' and chess.chess_type=='duck')):
            chess.cur_cell.position=self.jump_po
            chess.sum+=4
            self.cur_chess.append(chess)
            return chess
        else:
            return None
    def checkFly(self,chess):
        if self.fly_po!=[] and ((self.color=='yellow' and chess.chess_type=='chick') or (self.color=='blue' and chess.chess_type=='hippo') or (self.color=='red' and chess.chess_type=='parrot') or (self.color=='green' and chess.chess_type=='duck')):
            chess.cur_cell.position=self.fly_po
            chess.sum+=12
            self.cur_chess.append(chess)
            return chess
        else:
            return None
    def checkCollide(self,chess):
        cur=chess.cur_cell
        if len(cur.cur_chess)>1:
            all_chess=[]
            for chess1 in cur.cur_chess:
                if chess1.chess_type!=chess.chess_type:
                    all_chess.append(chess1)
            if all_chess!=[]:
                return all_chess
        return None
