import re
from collections import defaultdict

class BagNode:
    def __init__(self, name):
        self.name = name
        self.quantities = defaultdict(lambda: 0)
        self.contents = defaultdict(lambda: None)

    def add_item(self, bag, amount):
        if self.contents[bag.name] is None:
            self.contents[bag.name] = bag
        self.quantities[bag.name] += amount

    def get_total_contents(self):
        # recursively check how many bags are in this bag 
        if self.quantities is None:
            return 1
        total = 0
        for (name,amount) in self.quantities.items():
            total += amount
            total += amount * self.contents[name].get_total_contents()
        return total

    def __getitem__(self, idx):
        return self.contents[idx]

def make_tree(data):
    # parse input data into tree structure, with individual bags
    # as nodes, and the leaves being the bags contained within each
    # bag

    # split rule string into lists for each bag in the rule
    name_format = lambda names: ' '.join(names)
    slice_rule = lambda line: [line[i:i+4] for i in range(0, len(line), 4)]
    rules = [slice_rule(rule.split()) for rule in data]

    # create a node for each possible bag
    key_bags = [rule[0] for rule in rules]
    key_bags = [BagNode(name_format(key_bag[0:2])) for key_bag in key_bags]
    key_bags = {bag.name:bag for bag in key_bags}

    for line in rules:
        bag, rest = line[0], line[1:]
        bag_id = name_format(bag[0:2])
        # get reference to bag object
        bag = key_bags[bag_id]

        for rule in rest:
            # terminal rule
            if rule[0] == 'no':
                break
            amount, name = int(rule[0]), rule[1:3]
            name = name_format(name)
            bag.add_item(key_bags[name], amount)

    return key_bags 

def check_bags(my_name, bag_keys, container_bags=set()):
    # recursion ends when we reach a bag with no contents
    for (name, bag) in bag_keys.items():
        if my_name in bag.contents.keys():
            container_bags.add(name)
            container_bags.update(check_bags(name, bag_keys, container_bags))
    return container_bags


def part1(data, my_bag):
    # check how many bags could contain my bag.
    # this includes bags containing those bags and so on
    bags = make_tree(data)
    container_bags = check_bags(my_bag, bags)
    return container_bags


def part2(data, my_bag):
    # find how many bags must be in my bag, including the bags 
    # in those bags and others recursively
    bags = make_tree(data)
    bag = bags[my_bag]
    return bag.get_total_contents()

if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    my_bag = 'shiny gold'

    out = part1(data, my_bag)
    print(f'part 1: {len(out)}')
    out = part2(data, my_bag)
    print(f'part 2: {out}')

