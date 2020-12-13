import re

def part1(earliest_depart, bus_ids):
    # find the first time a bus will depart after the earliest_depart time
    bus_ids = [int(x) for x in bus_ids if x != 'x']

    t = earliest_depart
    while True:
        # check the state of every bus
        arrivals = [not t%ids for ids in bus_ids]
        if any(arrivals):
            break
        t+=1
    print(earliest_depart, t, arrivals)
    return (t - earliest_depart) * bus_ids[arrivals.index(True)]

def part2(bus_ids):
    # brute force search that checks every increment
    # very fast, but does not scale well for big inputs

    # all examples take less than 50 ms including jit compilation, but the full input
    # requires near infinite amount of computation
    bus_ids = [int(x) if x != 'x' else 1 for x in bus_ids]
    inc = bus_ids[0]
    t = 0 
    state = [False] * len(bus_ids)
    terminal = [True] * len(bus_ids)
    while True:
        t += inc 
        state = [not (t+i)%x for i,x in enumerate(bus_ids)]
        if state == terminal:
            break

    print(state)
    return t

def part2_crt(bus_ids):
    # took some googling to find out I had to formulate this as a symbolic 
    # number theory problem

    # if any of the bus_ids were not coprime, this solution would not work
    # see -> https://docs.sympy.org/latest/modules/ntheory.html
    from sympy.ntheory.modular import crt

    bus_ids = [int(x) if x != 'x' else 'x' for x in bus_ids]
    # moduli's
    M = [x for x in bus_ids if x != 'x']
    # residues. i.e. solving for t: residue = id mod t 
    # to calculate a residue, we need the bus id minus the offset from time t
    # then modulo with itself -> (id - offset) % id
    U = [(x-i) % x for (i,x) in enumerate(bus_ids) if x != 'x']

    # res is the smallest integer that satisfies all modulo rules.
    # and in this case we do not care about the least common multiple
    res, lcm = crt(M, U)
    return int(res)

def print_schedule(bus_ids):
    # print in a format useful for visualising the problem
    print('time',end='\t')
    for ids in bus_ids:
        print(ids, end='\t')
    print()
    for t in range(929, 949):
        print(t, end='\t')

        for ids in bus_ids:
            print('.' if t%ids else 'D', end='\t')

        print()


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines() if not l.isspace()]

    earliest_depart, bus_ids = int(data[0]), data[1].split(',')
    print(bus_ids)
    out = part1(earliest_depart, bus_ids)
    print(f'part 1: {out}')
    # find the earliest time for when each bus arrives sequentually
    out = part2_crt(bus_ids)
    print(f'part 2: {out}')
