from copy import deepcopy

class Program:
    def __init__(self, instructions, pc=0):
        self.instructions = instructions
        # program counter
        self.pc = pc 
        # instruction register
        self.ir = None
        self.acc = 0

    def run(self, catch_loop=True):
        stack = []
        while self.pc not in stack:
            if self.pc >= len(self.instructions):
                # return 0 if we execute all instructions
                return 0
            stack.append(self.pc)
            self.execute()

        # if a cycle is found in the instructions, the loop
        # will break, and the function returns a -1
        return -1

    def execute(self):
        # execute instruction pointed to by the pc
        self.ir = self.instructions[self.pc]
        op, value = self.ir

        if op == 'nop':
            self.pc += 1
        elif op == 'acc':
            self.pc += 1
            self.acc += value
        elif op == 'jmp':
            self.pc += value


def make_instructions(data):
    # parse input data in to operator/operand pairs
    instructions = [line.split(' ') for line in data]
    instructions = [[a[0], int(a[1])] for a in instructions]
    return instructions

def part1(data):
    # find the value of the program accumulator at the point where
    # a cycle is detected 
    instructions = make_instructions(data)
    program = Program(instructions)
    program.run()
    return program.acc

def part2(data):
    # find which jmp/nop instruction needs to be swapped for the
    # program to execute all lines
    # then return the value of the accumulator
    original_instructions = make_instructions(data)
    ops = [i[0] for i in original_instructions]
    swap_ops = ['nop','jmp']
    swaps = {swap_ops[0]:swap_ops[1], swap_ops[1]:swap_ops[0]}
    indices = [i for i, op in enumerate(ops) if op in swap_ops]

    for i in indices:
        # need deepcopy, as list.copy() does not propogate to sublists
        instructions = deepcopy(original_instructions)
        instructions[i][0] = swaps[instructions[i][0]]
        program = Program(instructions)
        code = program.run()
        if code == 0:
            return program.acc

    return -1
    


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines() if not l.isspace()]

    out = part1(data)
    print(f'part 1: {out}')
    out = part2(data)
    print(f'part 2: {out}')

