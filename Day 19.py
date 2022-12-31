import time
start_time = time.time()
inp = []
with open("sample.txt") as elf:
    # inp = elf.readlines()
    [inp.append(line) for line in elf.read().splitlines()]  # ..end(line.split" ")) for
blueprints = []  # ore, clay, obsidian, geode
quality = 0
cont = False
options = []
for k, line in enumerate(inp):
    blueprints.append([])
    for j in range(len(line)):
        if cont:
            cont = False
            continue
        if line[j].isdigit():
            if line[j + 1].isdigit():
                blueprints[k].append(int(line[j:j + 2]))
                cont = True
            else:
                blueprints[k].append(int(line[j]))

class paths:
    def __init__(self, min, goods, robots, blueprint, best, build):
        self.min = min
        self.goods = goods
        self.robots = robots
        self.blueprint = blueprint
        self.best = best
        self.build = build
    def robot(self):
        while self.min <= 24:
            if self.goods[3] + self.robots[3]*(25-self.min) + ((24-self.min)*(25-self.min)/2) <= self.best:
                return self.best
            # deciding what robot to build (where recursion will take place)
            if self.build[0] == 4:
                #geode conditions
                if self.robots[2]:
                    options.append("")
                    options[-1] = paths(self.min, self.goods, self.robots, self.blueprint, self.best, [3, False])
                #ore conditions
                if self.min < 22 and self.robots[0]*(22-self.min) + self.goods[0] < 22-self.min*(max(self.blueprint[1], self.blueprint[2], self.blueprint[4])):
                    options.append("")
                    options[-1] = paths(self.min, self.goods, self.robots, self.blueprint, self.best, [0, False])
                #obsidian conditions
                if self.robots[1] and self.min < 22 and self.robots[2]*(22-self.min) + self.goods[2] < 22-self.min*self.blueprint[5]:
                    options.append([])
                    options[-1] = paths(self.min, self.goods, self.robots, self.blueprint, self.best, [2, False])
                #clay conditions
                if self.min < 20 and self.robots[1]*(22-self.min) + self.goods[1] < 22-self.min*self.blueprint[3]:
                    options.append([])
                    options[-1] = paths(self.min, self.goods, self.robots, self.blueprint, self.best, [1, False])
                return self.best
            #starting production
            if (self.build[0] == 0 and self.goods[0] >= self.blueprint[0]) or (self.build[0] == 1 and self.goods[0] >= self.blueprint[1]) or\
                (self.build[0] == 2 and self.goods[0] >= self.blueprint[2] and self.goods[1] >= self.blueprint[3]) or (self.build[0] == 3 and self.goods[0] >= self.blueprint[4] and self.goods[2] >= self.blueprint[5]):
                self.build[1] = True
            #collecting self.goods
            for j in range(4):
                self.goods[j] += self.robots[j]
            #robot finish
            if self.build[1]:
                self.robots[self.build[0]] += 1
                if self.build[0] == 3:
                    self.goods[0] -= self.blueprint[4]
                    self.goods[2] -= self.blueprint[5]
                elif self.build[0] == 2:
                    self.goods[0] -= self.blueprint[2]
                    self.goods[1] -= self.blueprint[3]
                else:
                    self.goods[0] -= self.blueprint[self.build[0]]
                self.build = [4, False]
            #next self.minute
            self.min += 1
            if self.min == 24:
                self.best = max(self.best, self.goods[3] + self.robots[3])
                return self.best


for i in range(len(blueprints)):
    robots = [1, 0, 0, 0]
    goods = [0, 0, 0, 0]
    options = [paths(1, goods, robots, blueprints[i], 0, [4, False])]
    top = 0
    while len(options) > 0:
        if not len(options)%50:
            print(len(options))
        top = max((options[0].robot()), top)
        options.pop(0)
    print(i+1, top)
    quality += (i + 1) * top
print(quality)
print("My program took", time.time() - start_time, "to run")
