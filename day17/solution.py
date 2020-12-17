import numpy as np
import itertools
from collections import defaultdict

def adjacent(v):
    return [v-1,v,v+1]
def get_adjacent_idxs(x,y,z):
    n_x = adjacent(x)
    n_y = adjacent(y)
    n_z = adjacent(z)
    neighbours = np.array((n_z, n_x, n_y))

    #neighbours = list(np.array(np.meshgrid(*neighbours)).T.reshape(-1,3))
    #neighbours = list(itertools.product(*neighbours))
    xs,ys,zs = [],[],[]
    for x_ in n_x:
        for y_ in n_y:
            for z_ in n_z:
                if x_ == x and y_ == y and z_ == z:
                    continue
                else: 
                    xs.append(x_)
                    ys.append(y_)
                    zs.append(z_)
    return xs,ys,zs

if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [list(l.strip()) for l in f.readlines() if not l.isspace()]

    active, inactive = b'#', b'.'
    X,Y,Z,N = 100,100,100,6
    grid  = np.full((Z,X,Y),b'.', dtype=np.dtype('S1'))
    coord = lambda x,lim: (lim // 2) + x 

    z = coord(0, Z)
    for i,row in enumerate(data):
        rescale = len(row) // 2
        for j,val in enumerate(row):
            x = coord(i - rescale,X)
            y = coord(j - rescale,Y)
            grid[z,x,y] = val 
   
    
    for t in range(1,N+1):
        grid_t = grid.copy()
        inactive_shared = defaultdict(lambda: 0)
        actives = np.argwhere(grid == active)
        print(f'{len(actives)} active')
        for z,x,y in actives:
            xs, ys, zs = get_adjacent_idxs(x,y,z)
            #neighbours.remove((z,x,y))
            #neighbours = grid[(zs,xs,ys)]

            n_active = 0
            for x_,y_,z_ in zip(xs,ys,zs):
                if grid[z_,x_,y_] == active:
                    n_active += 1
                else:
                    inactive_shared[(z_,x_,y_)] += 1

            if not(n_active == 2 or n_active == 3):
                grid_t[z,x,y] = inactive
            #neighbours = np.take(grid,[[1,1,0],[1,1,1]])
        for (z,x,y), adj in inactive_shared.items():
            if adj == 3:
                grid_t[z,x,y] = active
        grid = grid_t
        print(f't {t}',(grid==active).sum())

