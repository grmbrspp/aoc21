import time

begin = time.time()

###

def tuple_sum(t: tuple, s: tuple) -> tuple:
	return tuple(a+b for a,b in zip(t,s))

def is_low_point(point: tuple) -> bool:
	adj_heights = [HEIGHTMAP[q] for q in ADJACENCIES[point]]
	return HEIGHTMAP[point] < min(adj_heights)

def get_basin(low_point: tuple) -> set:
	basin = set()
	edge = [low_point]
	while edge:
		basin.update(edge)
		edge = [q for p in edge for q in ADJACENCIES[p]
				if q not in basin and HEIGHTMAP[q] < 9]
	return basin


HEIGHTMAP = {}
with open("input.txt") as file:
	for y, line in enumerate(file):
		for x, height in enumerate(line.strip()):
			HEIGHTMAP[(x,y)] = int(height)

adj_mask = [(0,1), (0,-1), (1,0), (-1,0)]
ADJACENCIES = {
	p: [tuple_sum(p,q) for q in adj_mask
		if tuple_sum(p,q) in HEIGHTMAP]
	for p in HEIGHTMAP
}

low_points = [p for p in HEIGHTMAP if is_low_point(p)]
basin_sizes = [len(get_basin(p)) for p in low_points]
basin_sizes.sort()

print(f"Part 1: {sum(1+HEIGHTMAP[p] for p in low_points)}")
print(f"Part 2: {basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]}")

###

end = time.time()
print(f"Runtime: {end - begin}")
