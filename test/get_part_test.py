# 算法3测试
from Board import Board
from GoAI import GoAI

# 创建棋盘和AI
board = Board()
ai = GoAI(board)

# 获取位置32颜色1连成的整体
p = ai.get_part(3, 2, 1)
for o in p:
    print(o.x,o.y)