import time
import re

begin = time.time()

###

def reverse_gauss(n: int) -> int:
	i, acc = 0, 0
	while acc <= n:
		i, acc = i+1, acc+i+1
	return i

def target_can_be_reached(pos: tuple, target_area: tuple) -> bool:
	x, y = pos
	_, max_x, min_y, _ = target_area
	return x <= max_x and min_y <= y

def is_in_target_area(pos: tuple, target_area: tuple) -> bool:
	x, y = pos
	min_x, max_x, min_y, max_y = target_area
	return min_x <= x <= max_x and min_y <= y <= max_y

def get_trajectory(x_velocity: int, y_velocity: int, target_area: tuple) -> list:
	result = []
	pos = (0,0)
	while target_can_be_reached(pos, target_area):
		pos = (pos[0] + x_velocity, pos[1] + y_velocity)
		result.append(pos)
		if is_in_target_area(pos, target_area):
			return result
		x_velocity -= 1 if x_velocity > 0 else 0
		y_velocity -= 1
	return None


with open("input.txt") as file:
	input_string = file.read().strip()

pattern = re.compile(r"-?\d+")
target = tuple(int(match) for match in re.findall(pattern, input_string))

min_x_velocity = reverse_gauss(target[0])
max_x_velocity = target[1]
min_y_velocity = target[2]
max_y_velocity = target[3] + target[1]

trajectories = [get_trajectory(x_vel, y_vel, target)
				for x_vel in range(min_x_velocity, max_x_velocity+1)
				for y_vel in range(min_y_velocity, max_y_velocity+1)]
valid_trajectories = [t for t in trajectories if t]
highest_y_positions = [max(t, key=lambda p: p[1])[1] for t in valid_trajectories]

print(f"Part 1: {max(highest_y_positions)}")
print(f"Part 2: {len(valid_trajectories)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
