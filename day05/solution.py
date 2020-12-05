import math

def get_passes(data):
    # need to split input to get seat row/column,
    # then convert from binary to decimal to get 
    # the id 
    lookup = {'B':'1','R':'1','F':'0','L':'0'}
    passes = {'rows':[],'cols':[]}
    for p_current in data:
        #B=1,F=0 
        #R=1,L=0
        p_current = ''.join([lookup[c] for c in p_current])
        row,col = p_current[:7],p_current[7:]
        passes['rows'].append(int(row,2))
        passes['cols'].append(int(col,2))
    return passes


def part1(data, id_callback=lambda r,c: r*8+c):
    # convert all pass data to ids
    passes = get_passes(data)
    ids = [id_callback(r,c) for (r,c) in zip(*passes.values())]
    return ids

def part2(data):
    # find the missing id that lies between two consecutive ids
    ids = part1(data)
    ids.sort()
    for idx in range(len(ids)-2):
        # a+1 = b = c-1
        if (ids[idx+1] - ids[idx] == 2):
            return ids[idx]+1
    else: 
        return -1

if __name__=='__main__':
    #data = ['FBFBBFFRLR','BFFFBBFRRR','FFFBBBFRRR','BBFFBBFRLL']
    with open('input.txt','r') as f:
        data = [l.strip() for l in f.readlines()]
    
    out = part1(data)
    print(f'part 1, max id is {max(out)}')
    out = part2(data)
    print(f'part 2, my id is {out}')

