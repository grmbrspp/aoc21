import time
import re

begin = time.time()

###

def add_n_to_next_regular_number(n: int, sfn: list, idx_generator) -> None:
	for idx in idx_generator:
		if isinstance(sfn[idx], int):
			sfn[idx] = n + sfn[idx]
			return

def explode(sfn: list) -> bool:
	depth = 0
	for idx, char in enumerate(sfn):
		if char == "[":
			depth += 1
		if char == "]":
			depth -= 1
		if depth > 4:
			add_n_to_next_regular_number(sfn[idx+1], sfn, range(idx,-1,-1))
			add_n_to_next_regular_number(sfn[idx+3], sfn, range(idx+5,len(sfn)))
			sfn[idx] = 0
			for _ in range(4):
				sfn.pop(idx+1)
			return True
	return False

def split(sfn: list) -> bool:
	for idx, char in enumerate(sfn):
		if isinstance(char, int) and char > 9:
			n = int(char)
			pair = ["[", n//2, "," , n//2 + int(n%2 > 0), "]"]
			sfn.pop(idx)
			for new_char in reversed(pair):
				sfn.insert(idx, new_char)
			return True
	return False

def reduced(sfn: list) -> list:
	while explode(sfn) or split(sfn):
		pass
	return sfn

def add_sfns(a: list, b: list) -> list:
	return ["["] + a + [","] + b + ["]"]

def get_magnitude(sfn_str: str) -> int:
	pair = re.compile(r"\[\d,\d\]")
	if pair.match(sfn_str):
		return 3*int(sfn_str[1]) + 2*int(sfn_str[3])
	if len(sfn_str) < 2:
		return int(sfn_str)
	depth = 0
	for idx, char in enumerate(sfn_str):
		if char == "[":
			depth += 1
			continue
		if char == "]":
			depth -= 1
			continue
		if depth == 1 and char == ",":
			split_idx = idx
			break
	return 3*get_magnitude(sfn_str[1:split_idx]) + 2*get_magnitude(sfn_str[split_idx+1:-1])

def get_total_sum(sfns: list) -> list:
	acc = None
	for sfn in sfns:
		if not acc:
			acc = sfn
			continue
		acc = add_sfns(acc, sfn)
		acc = reduced(acc)
	return acc

input_numbers = []
NON_NUMERIC_CHARS = {"[", "]", ","}
with open("input.txt") as file:
	for line in file:
		snailfish_number = []
		for character in line.strip():
			if character in NON_NUMERIC_CHARS:
				snailfish_number.append(character)
			else:
				snailfish_number.append(int(character))
		input_numbers.append(snailfish_number)

total_sum = get_total_sum(input_numbers)
sums_of_two = [add_sfns(a,b) for a in input_numbers for b in input_numbers]
reduced_sums = [reduced(sfn_sum) for sfn_sum in sums_of_two]
magnitudes = [get_magnitude("".join(str(char) for char in sfn_sum)) for sfn_sum in reduced_sums]

print(f"Part 1: {get_magnitude(''.join(str(char) for char in total_sum))}")
print(f"Part 2: {max(magnitudes)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
