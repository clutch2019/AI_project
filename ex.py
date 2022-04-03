# a = '123'
# b = '123'
# # print(a==b)
# a = [12,34,67]
#
# a.pop(0)
#
# print(a)

def h3(now, goal):
    """

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
    print(new_now)
    for i in range(len(new_now)):
        for j in range(i+1, len(new_now)):
            if new_now[i] > new_now[j]:
                tot += 1

    return tot


def h2(now, goal):
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

if __name__ == "__main__":
    now = '468071235'
    goal = '462358071'
    # print(now.replace('0', ''))
    print(h2(now, goal))