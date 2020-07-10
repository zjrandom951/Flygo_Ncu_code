# 电脑下围棋算法:围棋是一种棋盘下法
from AI import AI
from Pointer import Pointer


# 围棋规则和下法
class GoAI(AI):
    # 重载父类构造方法
    def __init__(self, board):
        self.board = board

        # 已经访问的节点的集合
        self.history = []

    # 算法一：计算1个棋子在x行y列处的气的个数（定义了什么是气）
    def get_qi(self, x, y):
        if self.board.get(x, y) == 0: return 0
        qi = 0
        # 上方
        if x - 1 >= 1 and self.board.get(x - 1, y) == 0: qi = qi + 1
        if x + 1 <= 19 and self.board.get(x + 1, y) == 0: qi = qi + 1
        if y + 1 <= 19 and self.board.get(x, y + 1) == 0: qi = qi + 1
        if y - 1 >= 1 and self.board.get(x, y - 1) == 0: qi = qi + 1
        return qi

    # 算法二：判断颜色c棋子在x行y列位置上是否成活（有气？）
    def is_live(self, x, y):
        return self.get_qi(x, y) != 0

    # 算法三（求整体算法）：求颜色c棋子在x行y列处连成整体的棋子的集合
    def get_part(self, x, y, c):
        if 1 <= x <= 19 and 1 <= y <= 19:
            # 访问棋子不为c,结束
            if self.board.get(x, y) != c: return []

            # 不能走回头路
            for p in self.history:
                if p.x == x and p.y == y:
                    return []

            self.history.append(Pointer(x, y))
            self.get_part(x, y - 1, c)  # 左走一步
            self.get_part(x, y + 1, c)  # 右走一步
            self.get_part(x - 1, y, c)  # 上走一步
            self.get_part(x + 1, y, c)  # 下走一步

        return self.history

    # 算法四(整体气算法)：计算颜色c在x行y列位置上连成整体的气的个数
    # 先求出整体，再计算整体中每颗棋子的气的和
    def get_part_qi(self, x, y, c):
        if self.board.get(x, y) == 0: return -1;  # 空点返回-1
        if self.board.get(x, y) != c: return -1;  # 颜色不同-1
        self.history = []
        part_qi = 0
        # 先求整体
        part = self.get_part(x, y, c)
        # 循环累加每个棋子的气
        for p in part:
            part_qi = part_qi + self.get_qi(p.x, p.y)
        return part_qi

    # 算法五（整体存活算法）
    def is_part_live(self, x, y, c):
        return self.get_part_qi(x, y, c) != 0

    # 算法六（禁着点判断算法）:判断颜色c在x,y处是否是禁着点
    def is_forbidden(self, x, y, c):
        self.board.set(x, y, c)
        if self.is_part_live(x, y, c): return False
        self.board.set(x, y, 0)
        print("禁着点")
        return True

    # 算法七（清除棋盘上没有气的子）
    def clear(self):
        print("全局气分布图")
        for i in range(1, 20):
            for j in range(1, 20):
                print(self.board.get(i, j), end=":")
                if self.board.get(i, j) != 0:
                    part_qi = self.get_part_qi(i, j, self.board.get(i, j))
                    print(part_qi, end="\t")
                    if part_qi == 0:
                        print("提子", end="")
                        self.history = []
                        part = self.get_part(i, j, self.board.get(i, j))
                        for p in part:
                            self.board.set(p.x, p.y, 0)
                else:
                    print("\t", end="")
            print()

    # 算法八（空目判断，所谓空目就是没有被任何子围起来的交叉点）
    def is_free_mu(self, x, y):
        if self.board.get(x, y) != 0: return False
        self.history = []
        # 获取空点的整体，寻找边界
        mu = self.get_part(x, y, 0)
        up = 0
        down = 0
        right = 0
        left = 0
        for p in mu:
            print("目坐标:", p.x, p.y)
            if p.x == 19: down = 1
            if p.x == 1: up = 1
            if p.y == 19: right = 1
            if p.y == 1: left = 1
        return up == 1 and down == 1 and right == 1 and left == 1

    # 清除一个整体
    def clear_part(self, x, y, c):
        self.history = []
        part = self.get_part(x, y, c)
        for p in part:
            self.board.set(p.x, p.y, 0)

    # 劫存在和打劫算法：颜色c放在在xy处进行打劫判断，如果存在劫就清除之并成功返回标志
    def exists_jie(self, x, y, c):
        k = 1 if c == 2 else 2  # 黑色判断白色劫
        p = 0  # 默认没有劫
        self.board.set(x, y, c)
        arr = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # 定义4个方向向量
        for a in arr:
            if 1 <= x - 1 and x + 1 <= 19 and y - 1 >= 1 and y + 1 <= 19:
                if self.get_part_qi(x + a[0], y + a[1], k) == -1: return 0
                if self.get_part_qi(x + a[0], y + a[1], k) == 0:
                    print('s=', k, a[0], a[1])
                    p = 1
                    self.clear_part(x + a[0], y + a[1], k)
        if p == 0: self.board.set(x, y, 0)
        return p == 1

    # 算法九（目的个数计算）
