import numpy as np
from collections import defaultdict

def get_adjacent(state, x, y, max_x, max_y):
    # find the state of every adjacent seat to the one at x,y
    x_t, y_t = (1,0,-1), (1,0,-1)
    adjacent = [(x+x_, y+y_) for x_ in x_t for y_ in y_t]
    adjacent = [(i,j) for (i,j) in adjacent if i >= 0 and j >= 0 
                                            and (i,j) != (x,y) 
                                            and (i < max_x and j < max_y)]
    adjacent = [state[i,j] for (i,j) in adjacent]
    return adjacent 

def first_visible(state, x, y, max_x, max_y):
    # find the state of the first seat along each axis from x,y
    stops = (b'L', b'#')
    x_t, y_t = (1,0,-1), (1,0,-1)
    #create pairs for 
    adjacent = [(x_, y_) for x_ in x_t for y_ in y_t]
    visible = []
    for (i, j) in adjacent:
        # discard current location
        if (i,j) == (0,0):
            continue
        x_,y_ = x,y
        while True:
            x_ += i
            y_ += j
            
            # range checks
            if x_ < 0 or y_ < 0:
                break
            if (x_,y_) == (x,y):
                break
            if x_ >= max_x or y_ >= max_y:
                break

            space = state[x_,y_]
            if space in stops:
                # we have found a seat
                visible.append(space)
                break
    return visible

def shuffle_seats(data, max_occupied, callback):
    max_x, max_y = len(data), len(data[0])
    floor, empty, occupied = b'.', b'L', b'#'

    state_t = data.copy()
    # create a dictionary of which states we've seen prior
    # the key values being the hash of each state array
    seen_state = defaultdict(lambda: False)
    seen_state[state_t.tobytes()] = True
    while True:
        # state_t is what we are looking at
        # state_t1 is wht we are changing
        state_t1 = state_t.copy()
        for i in range(max_x):
            for j in range(max_y):
                space = state_t[i][j]
                if space == floor:
                    state_t1[i][j] = floor
                    continue

                states_adjacent = callback(state_t, i, j, max_x, max_y)

                # using rules specified in question
                if space == empty and occupied not in states_adjacent:
                    state_t1[i][j] = occupied
                elif space == occupied and states_adjacent.count(occupied) >= max_occupied:
                    state_t1[i][j] = empty
                else:
                    state_t1[i][j] = space

        # if we've seen this state before then stop execution 
        state_t1_b = state_t1.tobytes()
        if seen_state[state_t1_b]:
            return state_t1

        seen_state[state_t1_b] = True
        state_t = state_t1


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [list(l.strip()) for l in f.readlines() if not l.isspace()]
    
    data = np.array(data, dtype=np.dtype('S1'))

    out = shuffle_seats(data, 4, get_adjacent)
    print(f'part 1: final seating plan is:\n {out}')
    occupied = (out == b'#').sum()
    print(f'with {occupied} occupied seats')

    out = shuffle_seats(data, 5, first_visible)
    print(f'part 2: final seating plan is:\n {out}')
    occupied = (out == b'#').sum()
    print(f'with {occupied} occupied seats')
