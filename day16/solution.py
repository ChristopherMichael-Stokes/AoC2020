import re
import itertools
import numpy as np

def parse_rules(data):
    # split input data in to a dictionary of rules, tuple of values for my ticket, 
    # and a list of tuples for each other ticket
    rules = {}
    my_ticket = None
    other_tickets = []

    # create rule dictionary
    section_idx = 0
    for idx, line in enumerate(data):
        if line == '':
            section_idx = idx+1
            break
        name, values = line.split(': ')
        values = values.split(' or ')
        values = [tuple(map(int, value.split('-'))) for value in values]
        rules[name] = values

    # parse tickets
    split_ticket = lambda l: tuple(map(int, l.split(',')))
    section = 0 # 0 is my_ticket, 1 is other_tickets
    for line in data[section_idx:]:
        if line == '':
            section += 1
            continue
        if section == 0:
            if line[0] != 'y':
                my_ticket = split_ticket(line)
        elif section == 1:
            if line[0] != 'n':
                other_tickets.append(split_ticket(line))

    return rules, my_ticket, other_tickets

def satisfies_rule(v, rule):
    return any([mn <= v <= mx for (mn,mx) in rule])

def part1(rules, tickets):
    # find ticket values that do not satisfy any rule
    invalids = 0
    discard = set()
    for idx, ticket in enumerate(tickets):
        for v in ticket:
            rule_match = [satisfies_rule(v, rule) for rule in rules.values()]
            if not any(rule_match):
                invalids += v
                discard.add(idx)
    return invalids, [t for (i,t) in enumerate(tickets) if i not in discard]

def part2(rules, my_ticket, tickets, col_prefix):
    # find out which column maps to which rule.
    n_rules = len(rules)
    idx_to_rule = [None] * n_rules
    tickets = np.array(tickets)

    # figure out which rules are satisfied by each column
    valids = []
    for col_idx in range(n_rules):
        col = tickets[:,col_idx]
        valids.append([])
        for rule_name, vals in rules.items():
            mn, mx = vals[0]
            mn_1, mx_1 = vals[1]
            follows_rule = (((mn<=col) & (col<=mx)) | ((mn_1<=col) & (col<=mx_1))).all()
            if follows_rule:
                valids[col_idx].append(rule_name)
    
    rules_to_col = {}
    rules_followed = [len(v) for v in valids]
    while sum(rules_followed := [len(v) for v in valids]) > 0:
        # find column that only matches one rule, then eliminate that from
        # the rest of the list
        col = rules_followed.index(1)
        rule_name = valids[col][0]
        rules_to_col[rule_name] = col
        for col in valids:
            if rule_name in col: col.remove(rule_name) 

    prod = 1
    for rule_name, col in rules_to_col.items():
        if col_prefix in rule_name:
            prod *= my_ticket[col]
    return prod 

if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()] 

    rules, my_ticket, other_tickets = parse_rules(data)

    out, tickets = part1(rules, other_tickets)
    print(f'part 1: {out} is the sum of all invalid values')
    col_prefix = 'departure'
    out = part2(rules, my_ticket, tickets, col_prefix)
    print(f'part 2: {out} is the product of all {col_prefix} columns in my ticket')
