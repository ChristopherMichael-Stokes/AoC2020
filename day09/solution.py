import numpy as np
from collections import deque


def part1(data, stride):
    # find the element in data that is not equal to the 
    # sum of any two elements in the previous `stride` elements
    for i in range(len(data)-stride):
        window, y = data[i:stride+i], data[stride+i]
        # get outer sum of of window vector
        sums = np.add.outer(window,window)
        valid = np.isin(sums, y).any()

        if not valid:
           return y 
    return -1

def part2(data, sum_to):
    # find the contiguous elements that sum up to value
    # specified by `sum_to` argument

    # need deque here as we are pushing elements to the tail, 
    # then iteratively removing the head until the sum is less or equal
    # to the `sum_to` argument
    sum_vals = deque([data[0]])
    for idx in range(1,len(data)):
        while (csum := sum(sum_vals)) > sum_to:
            sum_vals.popleft()
        if csum == sum_to:
            break
        sum_vals.append(data[idx])
    else:
        # if for loop isn't broken out of
        return -1


    return min(sum_vals) + max(sum_vals)


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [int(l) for l in f.readlines() if not l.isspace()]
        data = np.array(data).astype(np.int32)

    out = part1(data, 25)
    print(f'part 1: {out}')
    out = part2(data, out)
    print(f'part 2: {out}')


