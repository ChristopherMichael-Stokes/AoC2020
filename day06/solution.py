from itertools import groupby
from collections import defaultdict
import re

def make_groups(data):
    # sort data into groups delimited by new lines
    groups = [list(g) for k,g in groupby(data, lambda x: x=='')]
    groups = [g for g in groups if g != ['']]
    return groups

def part1(data):
    # get sum of unique answers from each group
    groups = make_groups(data)
    groups = []
    for g in make_groups(data):
        group = []
        for item in g:
            group.extend([c for c in re.split(r'([a-z])',item) if c != ''])
        groups.append(set(group))

    return sum([len(g) for g in groups])

def part2(data):
    # get amount of answers each group unanimously voted on
    old_groups = make_groups(data)
    groups = []
    for group in old_groups:
        gs = defaultdict(lambda: 0)
        for item in group:
            for c in item:
                gs[c]+=1
        groups.append(gs)

    sums = []
    for idx, group in enumerate(groups):
        len_group = len(old_groups[idx])
        total = [1 for v in group.values() if v == len_group]
        sums.append(sum(total))
    return sum(sums)
        


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    out = part1(data)
    print(f'part1: {out}')
    out = part2(data)
    print(f'part2: {out}')





