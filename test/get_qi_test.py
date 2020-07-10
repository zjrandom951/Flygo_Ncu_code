# 算法1测试
from Board import Board
from GoAI import GoAI

# 创建棋盘和AI
board = Board()
ai = GoAI(board)

# 获取棋子的气的个数
qi = ai.get_qi(2, 2, 2)
print(qi)

# 判断存活
live = ai.is_live(2, 2, 2)
print(live)
