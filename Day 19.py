import time
import re
start_time = time.time()

with open("elves.txt") as elf:
    inp = elf.read().strip().splitlines()

blueprints = []  # ore, clay, obsidian, geode
quality = 0
cont = False
options = []
paths = []

for k, line in enumerate(inp):
    blueprints.append([int(s) for s in re.findall(r'-?\d+\.?\d*', line[30:])]) # The blueprint number gets added if including first 30 characters

class path:
    def __init__(self, tupl):
        self.minute = tupl[0]
        self.goods = tupl[1]
        self.robots = tupl[2]
        self.blueprint = tupl[3]
        self.best = tupl[4]
        self.build = tupl[5]


    def robot(self):
        while self.minute <= 25:
            if self.goods[3] + self.robots[3]*(25-self.minute) + ((24-self.minute)*(25-self.minute)/2) <= self.best:
                return self.best

            # deciding what robot to build (where recursion will take place)
            if self.build[0] == 4:
                #geode conditions
                if self.robots[2]:
                    self.best = max(path((self.minute, self.goods.copy(), self.robots.copy(), self.blueprint, self.best, [3, False])).robot(), self.best)
                #ore conditions
                if self.minute < 22 and self.robots[0]*(22-self.minute) + self.goods[0] < (22-self.minute)*(max(self.blueprint[1], self.blueprint[2], self.blueprint[4])):
                    self.best = max(path((self.minute, self.goods.copy(), self.robots.copy(), self.blueprint, self.best, [0, False])).robot(), self.best)
                #obsidian conditions
                if self.robots[1] and self.minute < 22 and self.robots[2]*(22-self.minute) + self.goods[2] < (22-self.minute)*self.blueprint[5]:
                    self.best = max(path((self.minute, self.goods.copy(), self.robots.copy(), self.blueprint, self.best, [2, False])).robot(), self.best)
                #clay conditions
                if self.minute < 20 and self.robots[1]*(22-self.minute) + self.goods[1] < (22-self.minute)*self.blueprint[3]:
                    self.best = max(path((self.minute, self.goods.copy(), self.robots.copy(), self.blueprint, self.best, [1, False])).robot(), self.best)
                return self.best

            #starting production
            if (self.build[0] == 0 and self.goods[0] >= self.blueprint[0]) or (self.build[0] == 1 and self.goods[0] >= self.blueprint[1]) or\
                (self.build[0] == 2 and self.goods[0] >= self.blueprint[2] and self.goods[1] >= self.blueprint[3]) or (self.build[0] == 3 and self.goods[0] >= self.blueprint[4] and self.goods[2] >= self.blueprint[5]):
                self.build[1] = True

            #collecting self.goods
            for j in range(4):
                self.goods[j] += self.robots[j]

            #robot finish (taking away goods and building robot)
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

            #next minuteute
            self.minute += 1
            if self.minute == 24:
                self.best = max(self.best, self.goods[3] + self.robots[3])
                return self.best


for i in range(len(blueprints)):
    robots = [1, 0, 0, 0]
    goods = [0, 0, 0, 0]
    top = path((1, goods, robots, blueprints[i], 0, [4, False])).robot()
    print(i+1, top)
    quality += (i + 1) * top
print(quality)
print("My program took", time.time() - start_time, "to run")
