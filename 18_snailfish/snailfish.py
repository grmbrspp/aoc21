import time
import re

begin = time.time()

###

NON_NUMERIC_CHARS = {"[", "]", ","}

def add_n_to_next_regular_number(n: int, sfn: list, idx_generator) -> None:
	for idx in idx_generator:
		if sfn[idx] not in NON_NUMERIC_CHARS:
			sfn[idx] = str(n + int(sfn[idx]))
			return

def explode(sfn: list) -> bool:
	depth = 0
	for idx, char in enumerate(sfn):
		if char == "[":
			depth += 1
		if char == "]":
			depth -= 1
		if depth > 4:
			add_n_to_next_regular_number(int(sfn[idx+1]), sfn, range(idx,-1,-1))
			add_n_to_next_regular_number(int(sfn[idx+3]), sfn, range(idx+5,len(sfn)))
			sfn[idx] = "0"
			for _ in range(4):
				sfn.pop(idx+1)
			return True
	return False

def split(sfn: list) -> bool:
	for idx, char in enumerate(sfn):
		if char not in ["[","]",","] and int(char) > 9:
			n = int(char)
			pair = ["[", str(int(n/2)), "," , str(int(n/2) + int(n%2 > 0)), "]"]
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
	for snailfish_number in sfns:
		if not acc:
			acc = snailfish_number
			continue
		acc = add_sfns(acc, snailfish_number)
		acc = reduced(acc)
	return acc

with open("input.txt") as file:
	input_numbers = [list(line.strip()) for line in file]

total_sum = get_total_sum(input_numbers)
sums_of_two = [add_sfns(a,b) for a in input_numbers for b in input_numbers]
reduced_sums_of_two = [reduced(sfn_sum) for sfn_sum in sums_of_two]
magnitudes = [get_magnitude("".join(sfn_sum)) for sfn_sum in reduced_sums_of_two]

print(f"Part 1: {get_magnitude(''.join(total_sum))}")
print(f"Part 2: {max(magnitudes)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
