import sys

aim = 0
horiz = 0
vert = 0
for line in sys.stdin:
    move, num = line.strip().split()
    if move == "forward":
        horiz += int(num)
        vert += aim * int(num)
    elif move == "down":
        # vert += int(num)
        aim += int(num)
    elif move == "up":
        # vert -= int(num)
        aim -= int(num)

print(horiz, vert, horiz * vert)
