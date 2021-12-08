import time

begin = time.time()

###

def get_unique_length_digit(digit_list: list, length: int) -> set:
	digit = next(dig for dig in digit_list if len(dig) == length)
	return set(digit)

def common_segment_count(a: set, b: set) -> int:
	return len(a.intersection(b))


unique_digits_count = 0
outputs = []
with open("input.txt") as file:
	for line in file:
		signal_patterns, out_val = [string.strip().split() for string in line.strip().split("|")]

		output = ""
		for digit in out_val:
			digit = set(digit)
			one, four = [get_unique_length_digit(signal_patterns, length) for length in (2,4)]
			match len(digit), common_segment_count(digit, one), common_segment_count(digit, four):
				case 2,_,_: output += "1"
				case 3,_,_: output += "7"
				case 4,_,_: output += "4"
				case 7,_,_: output += "8"
				case 5,2,_: output += "3"
				case 5,1,2: output += "2"
				case 5,1,3: output += "5"
				case 6,1,_: output += "6"
				case 6,2,3: output += "0"
				case 6,2,4: output += "9"

		unique_digits_count += sum(1 for digit in output if digit in {"1","4","7","8"})
		outputs.append(int(output))

print(f"Part 1: {unique_digits_count}")
print(f"Part 2: {sum(outputs)}")

###

end = time.time()
print(f"Runtime: {end - begin}")
