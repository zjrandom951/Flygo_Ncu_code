from Board import Board
from GoAI import GoAI

# 创建棋盘和AI
board = Board()
ai = GoAI(board)

r = ai.is_free_mu(5, 13)
print(r)
