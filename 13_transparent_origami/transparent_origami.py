import time

begin = time.time()

###


def fold(grid: set, instruction: tuple) -> set:
	result = set()
	modification_idx = 0 if instruction[0] == "x" else 1
	for dot in grid:
		if dot[modification_idx] > instruction[1]:
			new_coord = 2*instruction[1] - dot[modification_idx]
			new_dot = (new_coord, dot[1]) if modification_idx == 0 else (dot[0], new_coord)
			result.add(new_dot)
			continue
		result.add(dot)
	return result

def fold_all(grid: set, instructions: list) -> set:
	for instruction in instructions:
		grid = fold(grid, instruction)
	return grid


def print_dots(grid: set) -> str:
	result = ""
	x_dimension = list(sorted(grid, key=lambda dot: dot[0]))[-1][0]
	y_dimension = list(sorted(grid, key=lambda dot: dot[1]))[-1][1]
	for y in range(y_dimension+1):
		line = "\n"
		for x in range(x_dimension+1):
			line += "#" if (x,y) in grid else " "
		result += line
	return result

dots = set()
fold_instructions = []
with open("input.txt") as file:
	for line in file:
		if "," in line:
			coordinates = tuple((int(n) for n in line.strip().split(",")))
			dots.add(coordinates)
		if "=" in line:
			instr = line.strip().split()[-1].split("=")
			fold_instructions.append((instr[0], int(instr[1])))

finished_manual = fold_all(dots, fold_instructions)

print(f"Part 1: {len(fold(dots, fold_instructions[0]))}")
print(f"Part 2: {print_dots(finished_manual)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
