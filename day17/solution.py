import numpy as np
import itertools

if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [list(l.strip()) for l in f.readlines() if not l.isspace()]

    active, inactive = b'#', b'.'
    X,Y,Z,N = 3,3,3,1
    grid  = np.full((Z,X,Y),b'.', dtype=np.dtype('S1'))
    coord = lambda x,lim: (lim // 2) + x 

    z = coord(0, Z)
    for i,row in enumerate(data):
        rescale = len(row) // 2
        for j,val in enumerate(row):
            x = coord(i - rescale,X)
            y = coord(j - rescale,Y)
            grid[z,x,y] = val

    adjacent = lambda v: [v-1,v,v+1]
    for t in range(N):
        print(grid[z,x,y])
        actives = np.argwhere(grid == active)
        print(f'{len(actives)} active')
        for x,y,z in actives:
            n_x = adjacent(x)
            n_y = adjacent(y)
            n_z = adjacent(z)
            neighbours = np.array((n_z, n_x, n_y))

            neighbours = list(np.array(np.meshgrid(*neighbours)).T.reshape(-1,3))
            print(neighbours)
            neighbours.remove([z,x,y])
            print(neighbours)
            #neighbours = np.take(grid,neighbours)
            break
