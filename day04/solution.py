import re

def get_passports(data):
    # parse data entries seperated by new lines 
    # into dictionaries
    passports = []
    p_current = {}
    for idx, line in enumerate(data):
        if line == '':
            passports.append(p_current)
            p_current = {}
            continue

        line = line.split(' ')
        creds = [l.split(':') for l in line]
        p_current.update({k:v for (k,v) in creds})

    passports.append(p_current)
    return passports

def p_valid(passport, fields):
    # returns true if passport contains all fields
    return set([*passport]).issuperset(fields)

def valid_range(value, low, high):
    # returns true if value lies between high and low
    if not value.isnumeric():
        return False 

    value = int(value)
    if value < low or value > high:
        return False

    return True


def part1(data, fields):
    # count the passports containing all specified fields
    passports = get_passports(data)
    valid = [p_valid(p, fields) for p in passports]
    return sum(valid)

def part2(data, fields):
    passports = get_passports(data)
    valid_passports = []
    
    # count the passports containing all specified fields,
    # and values for all fields are valid
    for p in passports:
        if not p_valid(p, fields):
            continue
        p_current = {}
        
        p_current['byr'] = valid_range(p['byr'],1920,2002)
        p_current['iyr'] = valid_range(p['iyr'],2010,2020) 
        p_current['eyr'] = valid_range(p['eyr'],2020,2030)            
        
        length, units = p['hgt'][0:-2], p['hgt'][-2:]
        if units == 'cm':
            p_current['hgt'] = valid_range(length, 150, 193)
        elif units == 'in':
            p_current['hgt'] = valid_range(length, 59, 76)
        else:
            p_current['hgt'] = False     
        
        # starts with '#', has exactly 6 valid characters
        p_current['hcl'] = re.match(r'^#[a-f0-9]{6}$', p['hcl']) is not None        
        p_current['ecl'] = p['ecl'] in ['amb','blu','brn','gry','grn','hzl','oth']
        p_current['pid'] = (p['pid'].isnumeric()) and (len(p['pid']) == 9)
        
        # print(p_current.items())
        if all(p_current.values()):
            valid_passports.append(p)

    return len(valid_passports)


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    fields = set(['byr', 'iyr', 'eyr', 'hgt', 
                  'hcl', 'ecl', 'pid'])

    out = part1(data, fields)
    print(f'part 1: {out} passports are valid')
    out = part2(data, fields)    
    print(f'part 2: {out} passports are valid')
    
 