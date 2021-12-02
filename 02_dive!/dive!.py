import time

begin = time.time()

###

with open("input.txt") as file:
	course = [line.strip() for line in file]

h, d1, d2 = 0, 0, 0
for instr in course:
	match instr.split():
		case "forward", n:
			h += int(n)
			d2 += d1*int(n)
		case "up", n:
			d1 -= int(n)
		case "down", n:
			d1 += int(n)

print(f"Part 1: {h * d1}")
print(f"Part 2: {h * d2}")

###

end = time.time()
print(f"Runtime: {end - begin}")
