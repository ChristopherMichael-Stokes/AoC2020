import numpy as np

def make_env(data):
    env = np.empty((len(data), len(data[0])), dtype='|S1')
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            env[i, j] = c
    return env

class Sled:
    def __init__(self,x=0,y=0,x_dir=1, y_dir=1):
        self.x = x
        self.y = y
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.path = []

    def move(self, steps, max_y):
        if steps == 1:
            return
        if self.y >= max_y:
            return
        self.x += self.x_dir; self.y += self.y_dir 
        self.path.append((self.x, self.y))
        self.move(steps-1, max_y)


def part1(data, x_=3, y_=1):
    # work out how many 'trees' are encountered when
    # moving from the top to the bottom of the env 
    # with the path determined by x increase and y increase
    clearing = b'.'
    tree = b'#'

    sled = Sled(x_dir=x_,y_dir=y_)
    env = make_env(data)

    steps = env.shape[0]
    sled.move(steps, steps)
    trees = 0
    for pos in sled.path:
        x, y = pos
        # the env repeats infinitely to the right
        x %= env.shape[1]
        y %= env.shape[0]
        trees += env[y, x] == tree

    return trees 


def part2(data):
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = 1

    for slope in slopes:
        trees *= part1(data, *slope)

    return trees


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    out = part1(data)
    print(f'part 1: {out} trees were encountered')
    out = part2(data)
    print(f'part 2: {out} trees were encountered')

