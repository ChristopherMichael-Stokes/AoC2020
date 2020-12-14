import re
from collections import defaultdict

def part1(data):
    # find the sum of the contents of the memory after applying the most current
    # transformation

    # emulating virtual memory with a dict so we only have references
    # to what is actually in use, otherwise we would need 2^36 ~ 512GiB of ram!!
    word_len = 36
    memory = defaultdict(lambda: 0)
    addr_re = re.compile('[0-9]+')
    for line in data:
        l,r = line.split(' = ')
        if l == "mask":
            mask = r
        else:
            addr = int(addr_re.findall(l)[0])
            value = int(r)
            # need to reverse due to endianness
            for i, b in enumerate(mask[::-1]):
                if b == '1':
                    # set value at i to 1
                    value |= 1 << (i)
                elif b == '0':
                    # set value at i to 0
                    value &= ~(1 << (i))
            memory[addr] = value
    return sum(memory.values())

def permutate_address(address, idxs):
    # depth first function to return all variations of the input bits at input idxs
    # returns 2**len(idxs) unique values
    # N.B. does not scale well with the amount of idxs, although is is no problem
    # for the input questions.  
    # A solution would be to refactor into left recursion then use memoisation
    if len(idxs) == 1:
        idx, rest = idxs[0], None
    else:
        idx, rest = idxs[0], idxs[1:]

    addr_1 = address | (1 << idx)
    if len(idxs) == 1:
        return [addr_1]
    else:
        return [addr_1] + permutate_address(addr_1, rest) + permutate_address(address, rest)

def part2(data):
    # similar to part1, but the transformations now apply to addresses rather
    # than the values to be written.  After the transformation, one address
    # can alias to multiple other addresses
    word_len = 36
    memory = defaultdict(lambda: 0)
    addr_re = re.compile('[0-9]+')
    for line in data:
        l,r = line.split(' = ')
        if l == "mask":
            mask = r
        else:
            value = int(r)
            addr = int(addr_re.findall(l)[0])
            idxs = []
            # need to reverse due to endianness
            for i, b in enumerate(mask[::-1]):
                if b == '1':
                    # set value at i to 1
                    addr |= 1 << (i)
                elif b == 'X':
                    addr &= ~(1 << i)
                    idxs.append(i)
            addresses = [addr] + permutate_address(addr, idxs)
            for addr in addresses:
                memory[addr] = value
    return sum(memory.values())


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines() if not l.isspace()]


    out = part1(data)
    print(f'part 1: {out}')
    out = part2(data)
    print(f'part 2: {out}')

