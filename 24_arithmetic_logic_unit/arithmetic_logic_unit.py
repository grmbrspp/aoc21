import time
from collections import defaultdict

begin = time.time()

###

def alu(program: list, inp: str) -> int:
	memory = defaultdict(int)
	inp = list(inp)
	for instruction in program:
		match instruction:
			case "inp", a:
				memory[a] = int(inp.pop(0))
			case "add", a, b:
				if b not in ["w","x","y","z"]:
					memory[a] += int(b)
				else:
					memory[a] += memory[b]
			case "mul", a, b:
				if b not in ["w","x","y","z"]:
					memory[a] *= int(b)
				else:
					memory[a] *= memory[b]
			case "div", a, b:
				if b not in ["w","x","y","z"]:
					memory[a] = memory[a] // int(b)
				else:
					memory[a] = memory[a] // memory[b]
			case "mod", a, b:
				if b not in ["w","x","y","z"]:
					memory[a] = memory[a] % int(b)
				else:
					memory[a] = memory[a] % memory[b]
			case "eql", a, b:
				if b not in ["w","x","y","z"]:
					memory[a] = int(memory[a] == int(b))
				else:
					memory[a] = int(memory[a] == memory[b])
	return memory["z"]


with open("input.txt") as file:
	prog = [tuple(line.strip().split()) for line in file]

# solved by hand
p1_solution = "98491959997994"
p2_solution = "61191516111321"

if alu(prog, p1_solution) == 0:
	print(f"Part 1: {p1_solution}")

if alu(prog, p2_solution) == 0:
	print(f"Part 2: {p2_solution}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
