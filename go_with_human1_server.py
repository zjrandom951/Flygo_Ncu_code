# 双人对战围棋游戏
import _thread

import pygame
import os
# 初始化屏幕（大小、标题、背景）
from Board import Board
from GoAI import GoAI
import socket

# 网络连接(服务端)
s = socket.socket()  # 创建 socket 对象
host = socket.gethostname()  # 获取本地主机名
port = 12345  # 设置端口
s.bind((host, port))  # 绑定端口
s.listen(5)  # 等待客户端连接
print("等待客户端连接...")
client, addr = s.accept()  # 建立客户端连接

# -------------------------------------------------
# name = input("请输入名字：")
# test_mode=input("开启调试模式吗?(1、开启，2、关闭)")
test_mode = 0  # 调试模式
name = "小明"
# 绘制信息面板
t = "01:23:32"
px = "a"
py = "6"
qi = 0

# --------------------------------------------------
# 步数
step = 1
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 40)
screen = pygame.display.set_mode([600, 860])
pygame.display.set_caption("双人对战围棋")

# 创建棋盘
board = Board()
d = 30


# 显示文字
def drawText(x, y, text, size, c):
    font = pygame.font.SysFont('simsunnsimsun', size)
    text = font.render(text, 1, c)
    screen.blit(text, (x, y))


# 绘制横竖20条线
def drawGird():
    i = 0

    while i <= d * (19 - 1):

        # 参数：屏幕，颜色[r,g,b]，开始点[行像素坐标，列像素坐标]，结束点，粗细
        pygame.draw.line(screen, [0, 0, 0], [d, i + d], [d * 18 + d, i + d], 1)
        pygame.draw.line(screen, [0, 0, 0], [i + d, d], [i + d, d * 18 + d], 1)
        i = i + d


# 绘制圆形棋子：绘制x行y列颜色为c的棋子
def drawCir(x, y, c):
    # 棋子坐标->屏幕坐标
    pygame.draw.circle(screen, c, [(y - 1) * d + d, (x - 1) * d + d], int(d / 2))


# 重新绘制棋盘棋子
def drawGirdAndPoint():
    black = [0, 0, 0]
    white = [255, 255, 255]
    pygame.draw.rect(screen, [204, 102, 51], [0, 0, 600, 600], 0)
    drawGird()
    for i in range(1, 20):
        for j in range(1, 20):
            c = board.get(i, j)
            if c != 0:
                if c == 1: drawCir(i, j, black)
                if c == 2: drawCir(i, j, white)


# 信息面板
def updateInfo():
    pygame.draw.rect(screen, [0, 0, 0], [0, 610, 860, 860], 0)

    drawText(10, 610, "%s(人类)" % name, 40, (255, 0, 0))
    drawText(240, 615, "时长：%s" % t, 32, (255, 255, 255))
    drawText(490, 610, "等待对方..", 18, (255, 255, 255))
    drawText(10, 660, "步数：%s    平均：30'" % step, 32, (0, 255, 0))
    drawText(10, 700, "黑方 子数：30 目数：21 吃子：23", 32, (255, 255, 122))
    drawText(10, 740, "白方 子数：30 目数：20 吃子：43", 32, (255, 255, 122))
    drawText(10, 780, "总数：283  剩余：232", 32, (0, 100, 255))
    drawText(10, 820, "位置：%s，%s  气：%s  禁着:是 劫:是" % (px, py, qi), 32, (255, 0, 255))


# 围棋下棋程序
ai = GoAI(board)


# 接受网络信息
def receive():
    print("开始接受数据：")
    while True:

        s1 = client.recv(1024)
        s2 = str(s1, encoding="utf-8")
        board.set(int(s2.split(",")[0]), int(s2.split(",")[1]), 2)
        ai.clear()
        global step
        step = step + 1
        drawGirdAndPoint()
        updateInfo()
        drawCir((int)(s2.split(",")[0]), (int)(s2.split(",")[1]), [0, 255, 0])
        pygame.display.update()


# 开启线程
_thread.start_new_thread(receive, ())

# 进入游戏循环
while True:
    drawGirdAndPoint()
    updateInfo()
    # 循环获取事件
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            client.close()
            s.close()
            exit()
        # 鼠标单击
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print("屏幕坐标：", x, y)
            x = (int)((pygame.mouse.get_pos()[1] + 10) / d)
            y = (int)((pygame.mouse.get_pos()[0] + 10) / d)
            print("棋子坐标：", x, y)
            # 当前步数和颜色
            print("步数=", step)
            print("黑手" if step % 2 == 1 else "白手")
            print("是否空目：", ai.is_free_mu(x, y))
            c = 1 if step % 2 == 1 else 2
            if board.get(x, y) != 0:
                print("该位置上有子")
                break
            if step % 2 == 0:
                print("对方下")
                break

            # 打劫和禁着点判断
            jie = 0
            forbidden = 0
            if ai.exists_jie(x, y, c) != 0:
                print("有劫")
                jie = 1
                step = step + 1
                client.send(bytes("%s,%s" % (x, y), encoding="utf8"))
            else:
                # 禁着点判断
                if ai.is_forbidden(x, y, c): forbidden = 1

            # 不存在劫和禁着点就正常下子
            if jie == 0 and forbidden == 0:
                # 黑白轮流落子
                board.set(x, y, 1)

                # 剔除死子：计算每一格开始的相连的整体的气的和为0的位置，就提子
                ai.clear()
                step = step + 1
                client.send(bytes("%s,%s" % (x, y), encoding="utf8"))

        # 鼠标移动
        if event.type == pygame.MOUSEMOTION:
            x = (int)((pygame.mouse.get_pos()[1] + 10) / d)
            y = (int)((pygame.mouse.get_pos()[0] + 10) / d)
            px = str(x)
            py = str(chr(ord('a') + y - 1))
            ai.history = []
            part = ai.get_part(x, y, ai.board.get(x, y))
            qi = ai.get_part_qi(x, y, ai.board.get(x, y))

            for p in part:
                if test_mode == 1: drawCir(p.x, p.y, [189, 255, 189])
                # if ai.is_free_mu(p.x, p.y):
                #     drawCir(p.x, p.y, [0, 255, 0])
                # else:
                #     drawCir(p.x, p.y, [255, 0, 0])
            pygame.draw.circle(screen, [255, 255, 0], [(y - 1) * d + d, (x - 1) * d + d], int(d / 4))

            updateInfo()

        # 屏幕刷新
        pygame.display.update()
