# 算法3测试
from Board import Board
from GoAI import GoAI

# 创建棋盘和AI
board = Board()
ai = GoAI(board)

#求棋子82颜色为1的气的个数
qi = ai.get_part_qi(8, 2, 1)
print(qi)