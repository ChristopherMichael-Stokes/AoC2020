import numpy as np
from collections import defaultdict

def part1(x):
    # find how many elements have a gap of 3, and how many a gap of 1
    diff = lambda x,n: sum([1 for i in range(len(x)-1) if x[i+1]-x[i]==n])+1 
    diff_3, diff_1 = diff(x,3),diff(x,1)
    #print(diff_3)
    #print(diff_1)
    return diff_3 * diff_1

m_paths_to = defaultdict(lambda: 1)
def paths_to(x):
    global m_paths_to
    if len(x) == 1:
        return 1
    
    m_paths_to[0] = 0
    print(arrange(x))
        
cache = {}
def paths_to(i, data):
    # using dynamic programming
    # many calls to path_to function, but most are duplicate
    # so it is more efficient to store previous computations in
    # a cache
    global cache
    if i==len(data)-1:
        return 1
    if i in cache:
        return cache[i]
    cache[i] = 0
    for j in range(i+1, len(data)):
        if data[j]-data[i]<=3:
            cache[i]+=paths_to(j,data)
    return cache[i]
   
   
def part2(data):
    # find how many possible unique paths exist, following
    # the gap of 1-3 rule
    data = [0, *data, max(data)+3]
    out = paths_to(0,data)
    return out


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [int(l.strip()) for l in f.readlines() if not l.isspace()]
        data = np.array(data,dtype=np.uint8)
    data.sort()
    out = part1(data)
    print(f'part 1: {out}')
    out = part2(data)
    print(f'part 2: {out}')
    

