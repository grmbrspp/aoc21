import time

begin = time.time()

###

def move_cucumbers(cucumbers: dict, direction: str) -> tuple:
	result = {}
	movement = False
	for pos, c_dir in cucumbers.items():
		if c_dir != direction:
			result[pos] = c_dir
			continue
		x, y = pos
		new_pos = ((x+1)%X_SIZE,y) if direction == ">" else (x,(y+1)%Y_SIZE)
		if new_pos in cucumbers:
			result[pos] = c_dir
			continue
		result[new_pos] = c_dir
		movement = True
	return result, movement

cucumber_positions = {}
X_SIZE, Y_SIZE = 0, 0
with open("input.txt") as file:
	for y_coord, line in enumerate(file):
		Y_SIZE = y_coord + 1
		for x_coord, char in enumerate(line.strip()):
			X_SIZE = x_coord + 1
			if char == ".":
				continue
			cucumber_positions[(x_coord,y_coord)] = char

movement_right, movement_down = True, True
step_counter = 0
while movement_right or movement_down:
	step_counter += 1
	cucumber_positions, movement_right = move_cucumbers(cucumber_positions, ">")
	cucumber_positions, movement_down = move_cucumbers(cucumber_positions, "v")

print(f"Part 1: {step_counter}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
