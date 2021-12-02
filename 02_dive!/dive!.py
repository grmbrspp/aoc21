import time

begin = time.time()

###

with open("input.txt") as file:
	course = [line.strip() for line in file]

functions = {
	"forward": lambda n, aim: (n, 0, aim*n),
	"up": lambda n, aim: (0, -n, 0),
	"down": lambda n, aim: (0, n, 0)
}

h, d1, d2 = 0, 0, 0
for instr in course:
	fn, param = instr.split()
	change = functions[fn](int(param), d1)
	h, d1, d2 = \
		h + change[0], \
		d1 + change[1], \
		d2 + change[2]

print(f"Part 1: {h * d1}")
print(f"Part 2: {h * d2}")

###

end = time.time()
print(f"Runtime: {end - begin}")
