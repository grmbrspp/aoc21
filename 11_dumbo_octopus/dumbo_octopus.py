import time

begin = time.time()

###

def tuple_sum(t: tuple, s: tuple) -> tuple:
	return tuple(a+b for a,b in zip(t,s))

def perform_step() -> int:
	will_flash, has_flashed  = set(), set()

	for octopus, e_level in OCTOPUS_MAP.items():
		if e_level > 8:
			will_flash.add(octopus)
		else:
			OCTOPUS_MAP[octopus] += 1

	while will_flash:
		octopus = will_flash.pop()
		for neighbour in ADJACENCIES[octopus]:
			if OCTOPUS_MAP[neighbour] > 8 and neighbour not in has_flashed:
				will_flash.add(neighbour)
			else:
				OCTOPUS_MAP[neighbour] += 1
		has_flashed.add(octopus)

	for octopus in has_flashed:
		OCTOPUS_MAP[octopus] = 0

	return len(has_flashed)


OCTOPUS_MAP = {}
with open("input.txt") as file:
	for y, line in enumerate(file):
		for x, energy_level in enumerate(line.strip()):
			OCTOPUS_MAP[(x,y)] = int(energy_level)

adj_mask = [(0,1), (0,-1), (1,0), (-1,0), (1,-1), (-1,1), (1,1), (-1,-1)]
ADJACENCIES = {
	p: [tuple_sum(p,q) for q in adj_mask
		if tuple_sum(p,q) in OCTOPUS_MAP]
	for p in OCTOPUS_MAP
}

flash_counts_per_step = []
while not flash_counts_per_step or flash_counts_per_step[-1] < 100:
	flash_counts_per_step.append(perform_step())

print(f"Part 1: {sum(flash_counts_per_step[:100])}")
print(f"Part 2: {len(flash_counts_per_step)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
