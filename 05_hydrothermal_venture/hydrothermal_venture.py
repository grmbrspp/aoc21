import time

begin = time.time()

###

def get_step_size(i: int, j: int) -> int:
	if i == j:
		return 0
	return 1 if i < j else -1

def get_points_between(a: tuple, b: tuple, diagonals: bool) -> list:
	result = []
	x_step, y_step = get_step_size(a[0], b[0]), get_step_size(a[1], b[1])

	if not any([diagonals, x_step == 0, y_step == 0]):
		return result

	result.append(a)
	while a != b:
		a = (a[0] + x_step, a[1] + y_step)
		result.append(a)

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

overlaps = lambda vmap: sum(val > 1 for val in vmap.values())

vent_map_p1 = get_vent_map(vent_lines, False)
vent_map_p2 = get_vent_map(vent_lines, True)

print(f"Part 1: {overlaps(vent_map_p1)}")
print(f"Part 2: {overlaps(vent_map_p2)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
