import time

begin = time.time()

###

def fold(grid: set, instruction: tuple) -> set:
	result = set()
	axis, line_pos = instruction
	for x, y in grid:
		if axis == "x" and x > line_pos:
			result.add((2*line_pos - x, y))
			continue
		if axis == "y" and y > line_pos:
			result.add((x, 2*line_pos - y))
			continue
		result.add((x,y))
	return result

def fold_all(grid: set, instructions: list) -> set:
	for instruction in instructions:
		grid = fold(grid, instruction)
	return grid

def print_dots(grid: set) -> str:
	result = ""
	x_dimension = max(x for x,y in grid) + 1
	y_dimension = max(y for x,y in grid) + 1
	for y in range(y_dimension):
		line = "\n"
		for x in range(x_dimension):
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

after_first_fold = fold(dots, fold_instructions[0])
finished_manual = fold_all(dots, fold_instructions)

print(f"Part 1: {len(after_first_fold)}")
print(f"Part 2: {print_dots(finished_manual)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
