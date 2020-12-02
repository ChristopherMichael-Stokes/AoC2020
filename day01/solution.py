import numpy as np
import itertools

sum_match=2020

def part1(data, sum_match=sum_match):
    for i, x in enumerate(data):
        for j, y in enumerate(data):
            if i == j:
                continue
            elif sum_match == x + y:
                return x*y, x, y

def part2(data, sum_match=sum_match):
    combinations = list(itertools.combinations(data,3))
    for item in combinations:
        if sum(item) == sum_match:
            return item, np.prod(item)
    


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = np.array([l.strip() for l in f.readlines()], dtype=np.int32)

    product, x, y = part1(data)
    print('part 1:')
    print(f'product of {x} and {y} is {product}')
    print('part 2:')

    combination, product = part2(data)
    print(f'product of {combination} is {product}')


