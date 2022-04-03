start = [1,2,3,0,6,9,4,7,8]#九宫格初始状态
start = [2,1,3,4,5,6,7,8,0]
end = [1,2,3,4,0,6,7,8,9]#九宫格结束状态
end = [1,2,3,4,5,6,7,8,0]
empty = [0,0,0,0,0,0,0,0,0]
search = []#广度优先搜索到的九宫格状态
num = 0
for i in range(0,9):
    num = num*10 + start[i]
all_num = [num]#已经查验过的所有状态
floor_num = [0]#状态当前所在的查验层数
lastone = []#当前状态的来源状态所在search表中的位置
move = [+3,-3,+1,-1]

def judge(x,y):
    if y<0 or y>8:
        return False
    elif x%3 == 2 and y%3 == 0:
        return False
    elif x%3 == 0 and y%3 == 2:
        return False
    else:
        return True 

def comp(x,y):
    for i in range(len(x)):
        if x[i]!=y[i]:
            return True   #如果有不相等的就返回TRUE
    return False

def trans_add(x,y,p):
    temp = p[:]
    temp[x]=p[y]
    temp[y]=p[x]
    if exam(temp):
        search.append(temp)
        return True
    else:
        return False

def exam(str):
    a = 0
    for i in range(0,9):
        a = a*10+str[i]
    if all_num.count(a)>0:
        return False
    else:
        return True

def find():
    search.append(start)
    p = 0
    q = 1
    while p<q:  
        if comp(search[p],end):   
            loc = search[p].index(0)
            for i in move:
                if judge(loc,loc+i):
                    if trans_add(loc,loc+i,search[p]):
                        lastone.append(p)
                        floor_num.append(floor_num[p]+1)
                        q+=1
            p+=1
        else:
            return p
    return -1

goal = find()
step_num = floor_num[goal]
print('移动次数:',step_num)
process=[search[goal]]
for i in range(step_num):
    b = lastone[goal-1]
    process.append(search[b])
    goal = b
real = [process[step_num]]
print('初始态为:')
print(process[step_num])
for i in range(1,step_num+1):
    real.append(process[step_num-i])
    print('step'+str(i)+':')
    print(process[step_num-i])       

print(real)#最终过程列表
