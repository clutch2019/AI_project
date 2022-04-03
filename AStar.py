import copy

# import plot
# from plot import *


def form_array(x, n):
    """
    传入字符串，传出二维数组
    :param x: str 传入的字符串格式
    :param n: int 几维
    :return: list 二维数组
    """
    t = []
    for i in range(0, n * n, n):
        t.append(list(x[i:i + n]))
    return t


def form_str(x):
    """
    传入二维数组，传出字符串
    :param x: list
    :return: str
    """
    t = ''
    for i in x:
        t += ''.join(i)
    return t


def move(now, n):
    """
    找出可交换的方格
    :param now: 当前状态
    :param n: int 几维
    :return: 与0可交换的方格的列表，元素为字符串
    """
    flag = now.index('0')
    now = form_array(now, n)
    x_pos = flag // n
    y_pos = flag % n
    output = []
    try:
        new = copy.deepcopy(now)
        new[x_pos][y_pos], new[x_pos + 1][y_pos] = new[x_pos + 1][y_pos], new[x_pos][y_pos]
        output.append(form_str(new))

    except IndexError as e:
        pass

    try:
        if x_pos != 0:
            new = copy.deepcopy(now)
            new[x_pos][y_pos], new[x_pos - 1][y_pos] = new[x_pos - 1][y_pos], new[x_pos][y_pos]
            output.append(form_str(new))

    except IndexError as e:
        pass

    try:
        new = copy.deepcopy(now)
        new[x_pos][y_pos], new[x_pos][y_pos + 1] = new[x_pos][y_pos + 1], new[x_pos][y_pos]
        output.append(form_str(new))

    except IndexError as e:
        pass

    try:
        if y_pos != 0:
            new = copy.deepcopy(now)
            new[x_pos][y_pos], new[x_pos][y_pos - 1] = new[x_pos][y_pos - 1], new[x_pos][y_pos]
            output.append(form_str(new))

    except IndexError as e:
        pass

    return output


class Node:
    def __init__(self, status, h, g, father):
        """
        节点函数
        :param status: str 当前状态
        :param h: int 当前状态的h
        :param g: int 当前状态的g
        :param father: 父节点 Node
        """
        self.status = status
        self.h = h
        self.g = g
        self.father = father


class AStar:
    def __init__(self, start, goal, h):
        """
        :param start: str
        :param goal: str
        :param h: int 1,2,3代表h函数不一样
        """
        self.start_str = start
        self.goal_str = goal
        self.n = int(pow(len(start), 0.5))
        self.h = h

        # 初始化起点、终点、指针
        self.start_node = Node(start, self.h_cost()(self.start_str, self.goal_str), 0, None)
        self.goal_node = Node(goal, 0, 0, None)
        self.current_node = self.start_node

        self.openList = []
        self.closeList = []
        self.path_list = []  # 最后寻找路径列表
        self.final = None  # 终止点

    def judge(self, s):
        """
        生成除了空格之外的逆序数
        self.n 是 维数
        :param s: str
        :return:  int 逆序数
        """
        a = list(s)
        flag = a.index('0')
        a.remove('0')
        ans = 0
        for i in range(len(a)):
            for j in range(i):
                # if int(a[j]) > int(a[i]):
                if a[j] > a[i]:
                    ans += 1

        if self.n % 2 == 0:
            ans += flag // self.n + 1

        return ans

    def h1(self, now, goal):
        """
        h1函数：九宫格每个数字离最终位置的步数差的和
        :param now: str
        :param goal: str
        :return: int
        """
        now = list(now)
        goal = list(goal)
        tot = 0
        for i in range(len(now)):
            x_now_pos = i // self.n
            y_now_pos = i % self.n
            flag = goal.index(now[i])
            x_goal_pos = flag // self.n
            y_goal_pos = flag % self.n
            tot += abs(x_goal_pos - x_now_pos) + abs(y_goal_pos - y_now_pos)
        return tot

    def h2(self, now, goal):
        """
        h2函数：起点和终点，不一样的字符个数
        :param now: str
        :param goal: str
        :return: int
        """
        tot = 0
        for i in range(len(now)):
            if now[i] != goal[i]:
                tot += 1
        return tot

    def h3(self, now, goal):
        """
        h3函数：起点相对于终点的逆序数
        :param now: str
        :param goal: str
        :return: int
        """
        tot = 0
        num_dict = {}
        now = now.replace('0', '')
        goal = goal.replace('0', '')
        new_now = ''
        for i in range(len(goal)):
            num_dict[goal[i]] = str(i)

        for i in now:
            new_now += num_dict[i]
        for i in range(len(new_now)):
            for j in range(i + 1, len(new_now)):
                if new_now[i] > new_now[j]:
                    tot += 1

        return tot

    def h4(self, now, goal):
        return 10*self.h2(now, goal) + 0*self.h3(now, goal)

    def h_mix(self, now, goal, k, w1, w2):
        return k*(w1 * self.h2(now, goal) + w2 * self.h3(now, goal))

    def h_cost(self):
        """
        根据h参数不同，返回不同的估价函数
        :return:
        """
        if self.h == 1:
            return self.h1
        elif self.h == 2:
            return self.h2
        elif self.h == 3:
            return self.h3
        elif self.h == 4:
            return self.h4

    def node_in_openList(self, node):
        # 判断参数是否在open表中  node:Node
        for i in self.openList:
            if i.status == node.status:
                return True
        return False

    def node_in_closeList(self, node):
        # 判断参数是否在close表中  node:Node
        for i in self.closeList:
            if i.status == node.status:
                return True
        return False

    def str_in_openList(self, s):
        # 判断参数是否在open表中  s:str
        for i in self.openList:
            if i.status == s:
                return True
        return False

    def str_in_closeList(self, s):
        # 判断参数是否在close表中  s:str
        for i in self.closeList:
            if i.status == s:
                return True
        return False

    def goal_check(self, node):
        # 查看是否已达到终点
        if node.status == self.goal_str:
            return True
        return False

    def arrange(self):
        if self.judge(self.start_str) % 2 != self.judge(self.goal_str) % 2:
            print('逆序错误')
            # 如果逆序数出错，直接退出
            return False

        if self.goal_check(self.current_node):
            # 如果起点即终点
            self.final = self.current_node
            return True

        self.closeList.append(self.start_node)  # 初始化closeList，只有起点

        for i in move(self.current_node.status, self.n):
            # 初始化openList，有第二层的所有节点
            self.openList.append(Node(i, self.h_cost()(i, self.goal_str), 1, self.current_node))
        self.openList.sort(key=lambda x: x.h + x.g, reverse=False)  # 按评估函数排序，排序完每次pop0就是最小的

        while True:
            # for i in range(len(self.openList)):
                # print(form_array(self.openList[i].status, self.n))
            # print()
            # print()

            self.current_node = self.openList[0]  # 取出当前函数值最小的

            if self.goal_check(self.current_node):
                # 每次取出都要判断是否已达终点
                self.final = self.current_node
                return True

            self.closeList.append(self.current_node)
            self.openList.pop(0)
            # 上述操作更新当前节点、openList、closeList

            current_status_move = move(self.current_node.status, self.n)  # 查看当前状态的下一个状态有哪些（这里题目设置保证了列表非空）
            for i in current_status_move:
                if not self.str_in_openList(i) and not self.str_in_closeList(i):
                    # 如果不在open和close表里才需要添加
                    self.openList.append(
                        Node(i, self.h_cost()(i, self.goal_str), self.current_node.g + 1, self.current_node))
                else:
                    pass

            self.openList.sort(key=lambda x: x.h + x.g, reverse=False)  # 再次排序openList

    def path(self):
        # 生成路径列表并返回
        x = self.final
        while x:
            self.path_list.append(x.status)
            x = x.father
        return self.path_list


def main():
    question = AStar('123069478', '123409687', h=1)
    question.arrange()
    path = question.path()
    print(path)
    for i in path:
        print(i.status)


if __name__ == '__main__':
    main()
