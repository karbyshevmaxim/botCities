
with open('cities.txt', encoding="utf8") as f:
    lines = [line.rstrip('\n') for line in f]

cities = {}
for line in lines:
    line = line.lower()
    if line[0] not in cities:
        cities[line[0]] = {}
    if line[0:2] not in cities[line[0]]:
        cities[line[0]][line[0:2]] = []
    cities[line[0]][line[0:2]].append(line)