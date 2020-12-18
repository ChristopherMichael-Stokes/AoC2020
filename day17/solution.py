import numpy as np
import itertools
from collections import defaultdict


def get_adjacent_idxs(*dim):
    # find all adjcent points in n-dimensional integer space
    n_dim = [(d-1,d,d+1) for d in dim]
    neighbours = np.array(list(itertools.product(*n_dim)))
    dim_vals = [list(neighbours[:,i]) for i in range(neighbours.shape[1])]

    # find and remove original point
    for i in range(len(dim_vals[0])):
        val = tuple(dim_vals[j][i] for j in range(len(dim_vals)))
        if val == dim:
            for j in range(len(dim_vals)):
                del dim_vals[j][i]
            break
    return dim_vals


def part2(data, lim=30, N=6):
    # function is identical to part 1, just with added fourth dimension
    # where needed.
    # would be a good idea TODO refactor parts 1&2 to a general abitrary dimension function
    active, inactive = b'#', b'.'
    grid  = np.full((lim,lim,lim,lim),b'.', dtype=np.dtype('S1'))
    coord = lambda x,l: (l // 2) + x  # rescale x into the space allocated
    z = coord(0, lim)
    w = coord(0, lim)
    for i,row in enumerate(data):
        rescale = len(row) // 2
        for j,val in enumerate(row):
            x = coord(i - rescale,lim)
            y = coord(j - rescale,lim)
            grid[w,z,x,y] = val 
    # main iteration loop
    for t in range(1,N+1):
        grid_t = grid.copy()
        # dict used to store all '.'s that are shared across multiple points
        inactive_shared = defaultdict(lambda: 0)
        actives = np.argwhere(grid == active)
        # print(f'{len(actives)} active')
        for w,z,x,y in actives:
            xs, ys, zs, ws = get_adjacent_idxs(x,y,z,w)
            n_active = 0
            for x_,y_,z_,w_ in zip(xs,ys,zs,ws):
                if grid[w_,z_,x_,y_] == active:
                    n_active += 1
                else:
                    inactive_shared[(w_,z_,x_,y_)] += 1

            if not(n_active == 2 or n_active == 3):
                grid_t[w,z,x,y] = inactive
        for (w,z,x,y), adj in inactive_shared.items():
            if adj == 3:
                grid_t[w,z,x,y] = active
        grid = grid_t
        print(f't {t}',(grid==active).sum())
    return (grid==active).sum()

def part1(data, lim=30, N=6):
    active, inactive = b'#', b'.'
    grid  = np.full((lim,lim,lim),b'.', dtype=np.dtype('S1'))

    coord = lambda x,l: (l // 2) + x 
    z = coord(0, lim)
    for i,row in enumerate(data):
        rescale = len(row) // 2
        for j,val in enumerate(row):
            x = coord(i - rescale,lim)
            y = coord(j - rescale,lim)
            grid[z,x,y] = val 
   
    for t in range(1,N+1):
        grid_t = grid.copy()
        inactive_shared = defaultdict(lambda: 0)
        actives = np.argwhere(grid == active)
        # print(f'{len(actives)} active')
        for z,x,y in actives:
            xs, ys, zs = get_adjacent_idxs(x,y,z)
            n_active = 0
            for x_,y_,z_ in zip(xs,ys,zs):
                if grid[z_,x_,y_] == active:
                    n_active += 1
                else:
                    inactive_shared[(z_,x_,y_)] += 1

            if not(n_active == 2 or n_active == 3):
                grid_t[z,x,y] = inactive
        for (z,x,y), adj in inactive_shared.items():
            if adj == 3:
                grid_t[z,x,y] = active
        grid = grid_t
        print(f't {t}',(grid==active).sum())
    return (grid==active).sum()

if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [list(l.strip()) for l in f.readlines() if not l.isspace()]

    N = 6
    out = part1(data, N=N)
    print(f'part 1: {out} cells are active after {N} iterations')

    out = part2(data, N=N)
    print(f'part 2: {out} cells are active after {N} iterations')
