import time

begin = time.time()

###

def get_step_size(n: int, m: int) -> int:
	if n == m:
		return 0
	return 1 if n < m else -1

def get_points_between(a: tuple, b: tuple, diagonals: bool) -> list:
	result = []
	ax, ay, bx, by = *a, *b
	if not any([diagonals, ax == bx, ay == by]):
		return result

	x_step, y_step = get_step_size(ax, bx), get_step_size(ay, by)
	p = (ax, ay)

	while p != b:
		result.append(p)
		p = (p[0] + x_step, p[1] + y_step)

	result.append(p)
	return result

def get_vent_map(lines: list, diagonals: bool) -> dict:
	result = {}
	for l in lines:
		for point in get_points_between(*l, diagonals):
			result[point] = result.get(point, 0) + 1
	return result


vent_lines = []
with open("input.txt") as file:
	for line in file:
		points = [tuple(point.strip().split(",")) for point in line.split("->")]
		points = [(int(x), int(y)) for x, y in points]
		vent_lines.append(points)

overlaps = lambda vmap: sum(True for val in vmap.values() if val > 1)

vent_map_p1 = get_vent_map(vent_lines, False)
vent_map_p2 = get_vent_map(vent_lines, True)

print(f"Part 1: {overlaps(vent_map_p1)}")
print(f"Part 2: {overlaps(vent_map_p2)}")

###

end = time.time()
print(f"Runtime: {end - begin}")
