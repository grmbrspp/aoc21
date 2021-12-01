import time

begin = time.time()

###

with open("input.txt") as file:
	measurements = [int(line) for line in file]

increases = lambda lst: [True for idx, n in enumerate(lst[1:]) if n > lst[idx]]
windows = [sum(measurements[idx:idx+3]) for idx, _ in enumerate(measurements[:-2])]

print(f"Part 1: {len(increases(measurements))}")
print(f"Part 2: {len(increases(windows))}")

###

end = time.time()
print(f"Runtime: {end - begin}")
