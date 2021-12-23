import time

begin = time.time()

###

def cuboids_intersect(a: tuple ,b: tuple) -> bool:
	return a[0] <= b[1] and b[0] <= a[1] \
		and a[2] <= b[3] and b[2] <= a[3] \
		and a[4] <= b[5] and b[4] <= a[5]


def cuboid_intersection(a: tuple, b: tuple) -> tuple:
	return (
		max((a[0], b[0])), min((a[1], b[1])),
		max((a[2], b[2])), min((a[3], b[3])),
		max((a[4], b[4])), min((a[5], b[5])),
	)

def total_volume_after(cuboid_activation_steps: list) -> int:
	cuboid_collection = []
	for instr, *new_cub in cuboid_activation_steps:
		compensation_cuboids = []
		for sgn, cub in cuboid_collection:
			if cuboids_intersect(cub, new_cub):
				compensation_cuboids.append((-sgn, cuboid_intersection(cub, new_cub)))
		if instr == "on":
			cuboid_collection.append((1, tuple(new_cub)))
		cuboid_collection.extend(compensation_cuboids)
	cuboid_volume = lambda a: (abs(a[1]-a[0])+1) * (abs(a[3]-a[2])+1) * (abs(a[5]-a[4])+1)
	return sum(sgn * cuboid_volume(cub) for sgn, cub in cuboid_collection)


steps = []
with open("input.txt") as file:
	for line in file:
		step = [line[:3].strip()]
		for dim in line[3:].strip().split(","):
			step.extend([int(n) for n in dim[2:].split("..")])
		steps.append(tuple(step))

initialization_steps = [s for s in steps
						if max(s[1:]) < 51
						and min(s[1:]) > -51]

print(f"Part 1: {total_volume_after(initialization_steps)}")
print(f"Part 2: {total_volume_after(steps)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
