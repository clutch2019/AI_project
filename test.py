import AStar
from AStar import move
from matplotlib import pyplot as plt
import time
import random


def judge(s , n):
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

        if n % 2 == 0:
            ans += flag // n + 1

        return ans

def generation(n):
    """
    生成合法的测试元组
    :param n: int 维数
    :return:  tuple (start_str , goal_str)
    """
    ls = []
    for i in range(n*n):
        ls.append(str(i))
    while True:
        ls_1 = random.sample(ls , n*n)
        ls_2 = random.sample(ls , n*n)

        start_str = ''
        goal_str = ''
        for i in ls_1:
            start_str += str(i)
        for i in ls_2:
            goal_str += str(i)

        if judge(start_str , n) % 2 == judge(goal_str , n) % 2:
            return start_str , goal_str
        else:
            continue


class Node(AStar.Node):
    def __init__(self, status, h, g, father):
        super().__init__(status , h , g , father)
        
class Test:
    """
    测试类
    :param start: str 
    :param goal: str
    :param finding_method: 寻路方法
    :param h: int 选择h函数
    :param n: int 维数
    """
    def __init__(self, start , goal , finding_method , h , n):
        self.finding_method = finding_method
        self.h = h
        self.start = start
        self.goal = goal
        self.n = n
    def test(self):
        task = self.finding_method(self.start, self.goal, self.h)
        task.arrange()
        print(task.path())

class Campare:
    """
    多种算法比较、可视化
    :param number_of_spot: int 可视化散点图上散点数量
    :param n: int 维数
    """
    def __init__(self , number_of_spot , n):
        self.number = number_of_spot
        self.n = n
    def run(self):
        test_data = []
        for i in range(self.number):
            test_data.append(generation(self.n))
        standard_time_list = []
        for i in test_data:
            
            standard_time_start = time.time()

            task = Test(i[0] , i[1] , Standard , 0 , self.n)
            task.test()

            standard_time_end = time.time()
            standard_time_list.append(standard_time_end - standard_time_start)
        
        print(standard_time_list)

        Astar_time_list = []
        for i in test_data:
            
            Astar_time_start = time.time()

            task = Test(i[0] , i[1] , AStar.AStar , 1 , self.n)
            task.test()

            Astar_time_end = time.time()
            Astar_time_list.append(Astar_time_end - Astar_time_start)
        
        print(Astar_time_list)
        plt.plot(standard_time_list , standard_time_list)
        plt.plot(standard_time_list , Astar_time_list)

        


class Standard:
    def __init__(self , start , goal , h):
        """
        :param start: str
        :param goal: str
        :param n: int 问题维数
        """
        self.start = start
        self.goal = goal
        self.n = int(pow(len(start), 0.5))
        self.open_list = []
        self.closed_list = []
        self.current = Node(start , 0 , 0 , None)

    def arrange(self):
        if self.start == self.goal:
            return True
        
        # current = Node(self.start , 0 , 0 , None)

        self.closed_list.append(self.current)
        for i in move(self.start , self.n):
            new_node = Node(i , 0 , 0 , self.current)
            self.open_list.append(new_node)

        while True:
            self.current = self.open_list.pop(0)
            # print(self.current.status)
            if self.current in self.closed_list:
                continue
            else:
                if self.current.status == self.goal:
                    return True
                else:
                    self.closed_list.append(self.current)
                    for i in move(self.current.status , self.n):
                        new_node = Node(i , 0 , 0 , self.current)
                        self.open_list.append(new_node)
    
    def path(self):
        path_list = []
        while(self.current != None):
            path_list.append(self.current.status)
            self.current = self.current.father
        
        return path_list





if __name__ == "__main__":
    t = Campare(2 , 3)
    t.run()