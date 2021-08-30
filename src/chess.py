class chess:
    def __init__(self, chess_type, chess_num, chess_map):
        self.sum = None
        self.cur_cell = None
        self.chess_type = chess_type
        self.chess_num = chess_num
        self.chess_map = chess_map

    #更新前进后棋子已前进的步数与当前所在的cell
    def update(self,cell):
        self.cur_cell.deleteCurrentChess(self)
        if cell in self.chess_map:
            self.sum = self.chess_map.index(cell)
            self.cur_cell = cell # 实例化的某一cell，有 position, jump_po, fly_po, color

    def takeOff(self):
        pass
