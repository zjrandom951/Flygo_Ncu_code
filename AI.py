# 人机对战父类
class AI:

    # 人机对战是建立在棋盘之上
    def __init__(self, board):
        self.board = board

    # 定义如何下棋的抽象方法
    def next(self):
        pass
