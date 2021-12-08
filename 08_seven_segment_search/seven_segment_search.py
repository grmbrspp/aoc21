import time

begin = time.time()

###

def get_unique_length_digit(digit_list: list, length: int) -> set:
	digit = next(dig for dig in digit_list if len(dig) == length)
	return set(digit)

def find_digit_in_list(digit_list: list, condition) -> set:
	digit = next(dig for dig in digit_list if condition(dig))
	digit_list.remove(digit)
	return digit


outputs = []
with open("input.txt") as file:
	for line in file:
		signal_patterns, out_vals = [string.strip().split() for string in line.strip().split("|")]

		digit_map = {}
		digit_map["1"] = get_unique_length_digit(signal_patterns, 2)
		digit_map["4"] = get_unique_length_digit(signal_patterns, 4)
		digit_map["7"] = get_unique_length_digit(signal_patterns, 3)
		digit_map["8"] = get_unique_length_digit(signal_patterns, 7)

		five_seg_digits = [set(dig) for dig in signal_patterns if len(dig) == 5]
		six_seg_digits = [set(dig) for dig in signal_patterns if len(dig) == 6]

		digit_map["9"] = find_digit_in_list(six_seg_digits, digit_map["4"].issubset)
		digit_map["3"] = find_digit_in_list(five_seg_digits, digit_map["1"].issubset)
		digit_map["5"] = find_digit_in_list(five_seg_digits, digit_map["9"].issuperset)
		digit_map["6"] = find_digit_in_list(six_seg_digits, digit_map["5"].issubset)
		digit_map["2"] = five_seg_digits[0]
		digit_map["0"] = six_seg_digits[0]

		inverse_digit_map = {"".join(sorted(v)): k for k, v in digit_map.items()}
		output = "".join(inverse_digit_map["".join(sorted(val))] for val in out_vals)
		outputs.append(output)

unique_digits = ["1","4","7","8"]
print(f"Part 1: {sum(sum(out.count(dig) for dig in unique_digits) for out in outputs)}")
print(f"Part 2: {sum(int(o) for o in outputs)}")

###

end = time.time()
print(f"Runtime: {end - begin}")
