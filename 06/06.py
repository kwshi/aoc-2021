import collections as co

fish = co.Counter(map(int, input().strip().split(",")))

for _ in range(256):
    new = fish[0]
    for i in range(8):
        fish[i] = fish[i + 1]
    fish[8] = new
    fish[6] += new

print(sum(fish.values()))
