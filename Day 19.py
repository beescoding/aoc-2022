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

def path(minute, goods, robots, blueprint, best, build):
    while minute <= 25:
        if goods[3] + robots[3]*(25-minute) + ((24-minute)*(25-minute)/2) <= best:
            return best

        # deciding what robot to build (where recursion will take place)
        if build[0] == 4:
            #geode conditions
            if robots[2]:
                best = max(path(minute, goods.copy(), robots.copy(), blueprint, best, [3, False]), best)
            #ore conditions
            if minute < 22 and robots[0]*(22-minute) + goods[0] < (22-minute)*(max(blueprint[1], blueprint[2], blueprint[4])):
                best = max(path(minute, goods.copy(), robots.copy(), blueprint, best, [0, False]), best)
            #obsidian conditions
            if robots[1] and minute < 22 and robots[2]*(22-minute) + goods[2] < (22-minute)*blueprint[5]:
                best = max(path(minute, goods.copy(), robots.copy(), blueprint, best, [2, False]), best)
            #clay conditions
            if minute < 20 and robots[1]*(22-minute) + goods[1] < (22-minute)*blueprint[3]:
                best = max(path(minute, goods.copy(), robots.copy(), blueprint, best, [1, False]), best)
            return best

        #starting production
        if (build[0] == 0 and goods[0] >= blueprint[0]) or (build[0] == 1 and goods[0] >= blueprint[1]) or\
            (build[0] == 2 and goods[0] >= blueprint[2] and goods[1] >= blueprint[3]) or (build[0] == 3 and goods[0] >= blueprint[4] and goods[2] >= blueprint[5]):
            build[1] = True

        #collecting goods
        for j in range(4):
            goods[j] += robots[j]

        #robot finish (taking away goods and building robot)
        if build[1]:
            robots[build[0]] += 1
            if build[0] == 3:
                goods[0] -= blueprint[4]
                goods[2] -= blueprint[5]
            elif build[0] == 2:
                goods[0] -= blueprint[2]
                goods[1] -= blueprint[3]
            else:
                goods[0] -= blueprint[build[0]]
            build = [4, False]

        #next minuteute
        minute += 1
        if minute == 24:
            best = max(best, goods[3] + robots[3])
            return best


for i in range(len(blueprints)):
    robots = [1, 0, 0, 0]
    goods = [0, 0, 0, 0]
    top = path(1, goods, robots, blueprints[i], 0, [4, False])
    quality += (i + 1) * top
print("Part 1", quality)
print("Part 1 took", time.time() - start_time, "to run")
quality = 1
for i in range(3):
    robots = [1, 0, 0, 0]
    goods = [0, 0, 0, 0]
    top = path(-7, goods, robots, blueprints[i], 0, [4, False])
    quality *= top
print("Part 2", quality)
print("Part 1+2 took", time.time() - start_time, "to run")
