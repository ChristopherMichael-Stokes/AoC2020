import re


def get_splits(line):
        # e.g. input '1-3 a: abcde'
        character = re.search('[a-z]',line).group(0)
        policy, pword = re.split('[a-z]\:', line)
        x, y = [int(i) for i in policy.split('-')]
        return character, pword.strip(), x, y


def part1(data):
    # part 1 - with regex
    # find occurances of the key character in pword string,
    # ensuring that it is in between the min / max amount set
    valids = 0
    for line in data:
        character, pword, o_min, o_max = get_splits(line)
        occurances = len(re.findall(character, pword))
        valid = occurances >= o_min and occurances <= o_max
        valids += valid
        # print(character,o_min,o_max,pword, occurances)
    return valids

def part2(data):
    valids = 0
    for line in data:
        # password is only valid if in location x
        # or y exclusively
        character, pword, x, y = get_splits(line)
        # indexed from 1
        a, b = pword[x-1], pword[y-1]
        a, b = a == character, b == character
        # a xor b 
        valids += a^b
        

    return valids 



if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()]
    out = part1(data)
    print(f'Part 1\n{out} passwords are valid')

    out = part2(data)
    print(f'Part 2\n{out} passwords are valid')
