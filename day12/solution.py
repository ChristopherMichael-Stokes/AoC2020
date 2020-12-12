import re, math


class Navigator:
    # navigation controller abstract class 
    def __init__(self, x=0, y=0, *args, **kwargs):
        #first dimension is rows, second is columns
        #origin being the top left, and y scale grows downwards
        self.directions = {
                'N':(0,-1),
                'E':(1,0),
                'S':(0,1),
                'W':(-1,0)
                }
        self.directions_ = list(self.directions.keys())
        self.turns = {
                'L': lambda x,y: x-y,
                'R': lambda x,y: x+y
                }
        self.x = x
        self.y = y

    def get_loc(self):
        return abs(self.x) + abs(self.y)


class Ship(Navigator):
    def __init__(self, direction='E', *args,**kwargs):
        super().__init__(*args, **kwargs)

        self.direction = direction
        self.bearing = self.directions_.index(direction)

    def act(self, action, value):
        if action in self.turns.keys():
            # rotate forward pointing direction
            self.bearing = self.turns[action](self.bearing, (value // 90)) % 4 # value in - 0,1,2,3
            # figure out new direction
            self.direction = self.directions_[self.bearing]
            return

        # get the movement vector for either the direction we are facing or
        # the specified direction
        move_vec = self.directions[self.direction] if action == 'F' else self.directions[action]

        self.x += value * move_vec[0]
        self.y += value * move_vec[1]
        #print((action,value),(self.x,self.y))


def part1(instructions):
    ship = Ship()
    for instruction in instructions:
        ship.act(*instruction)
    return ship.get_loc()

class Waypoint(Navigator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ship_x = 0
        self.ship_y = 0

    def act(self, action, value):
        if action in self.turns.keys():

            # we know thetas can only be multiples of 90, so we can safely cast to int
            c_val, s_val  = int(math.cos(math.radians(value))), int(math.sin(math.radians(value)))
            if action == 'L':
                s_val = -s_val 
            x_pivot, y_pivot = self.x, self.y

            # rotate around origin
            self.x = (c_val * x_pivot - s_val * y_pivot)
            self.y = (s_val * x_pivot + c_val * y_pivot)
        elif action in self.directions.keys():
            # move in cardinal direction
            move_vec = self.directions[action] 
            self.x += value * move_vec[0]
            self.y += value * move_vec[1]
        elif action == 'F':
            # move ship toward waypoint
            self.ship_x += self.x * value
            self.ship_y += self.y * value

        #print((action,value),(self.x,self.y),(self.ship_x, self.ship_y))

    def get_loc(self):
        return abs(self.ship_x) + abs(self.ship_y)
        

def part2(instructions):
    waypoint = Waypoint(10, -1)
    for instruction in instructions:
        waypoint.act(*instruction)

    return waypoint.get_loc()


if __name__=='__main__':
    with open('input.txt', 'r') as f:
        data = [l.strip() for l in f.readlines() if not l.isspace()]

    instructions = [(l[0], int(l[1:])) for l in data]
    out = part1(instructions)
    print(f'part 1: {out}')
    out = part2(instructions)
    print(f'part 2: {out}')
