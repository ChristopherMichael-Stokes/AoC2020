from collections import defaultdict

def memory_game(start_list, N):
    # occurence dictionary to store time each a number is mentioned.
    # could be made more memory efficient by using a fixed size queue, as we 
    # only care about the two most recent occurences for each n
    occurences = defaultdict(lambda: [])

    for i, n in enumerate(start_list):
        occurences[n].append(i)
    last_spoken = start_list[-1]

    for t in range(len(start_list), N):
        # useful to print for large N
        if t % 1000 == 0:
            print(f'{t:010}', end = '\r')

        # apply game rules to find next number
        last_occurences = occurences[last_spoken]
        if last_occurences == [] or len(last_occurences) == 1:
            spoken = 0
        else:
            spoken = (t-1) - last_occurences[-2]

        occurences[spoken].append(t)
        last_spoken = spoken
    return last_spoken

if __name__=='__main__':
    start_list = [0,5,4,1,10,14,7]
    part1 = memory_game(start_list, 2020)
    print(f'part 1: last number spoken is {part1}')
    part2 = memory_game(start_list, 30_000_000)
    print(f'part 2: last number spoken is {part2}')
