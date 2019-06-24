import random
from itertools import combinations as cb

dic = {}
nums = list(range(1,26))
rang = range(5)
form = [[nums.pop(random.randint(0,len(nums)-1)) for _ in rang] for _ in rang]

for i in rang:
    for j in rang:
        dic[form[i][j]] = (i,j)

def isline(line):
    
    slash1 = set()
    slash2 = set()
    startVal = line[0]
    check = [1,1]
    for x,y in line:
        if x != startVal[0]:check[0] = 0
        if y != startVal[1]:check[1] = 0
        slash1.add(x+y)
        slash2.add(x-y)
        
    return check[0] or check[1] or \
           (len(slash1)==1 and 4 in slash1) or \
           (len(slash2)==1 and 0 in slash2)

leng = 0
correct = 0
for line in cb(list(range(1,26)),5):
    line = [dic[n] for n in line]
    if isline(line):correct+=1
    leng+=1

print(correct,'/',leng)
    
