import time

begin = time.time()

###

def most_common_val(arr: list, col_idx: int) -> int:
	col = [line[col_idx] for line in arr]
	avg = sum(col)/len(arr)
	return 1 if avg == 0.5 else round(avg)

def bin_array_to_int(arr: list) -> int:
	bin_str = "".join([str(elem) for elem in arr])
	return int(bin_str, 2)


with open("input.txt") as file:
	report = [[int(char) for char in line.strip()] for line in file]

h_size = len(report[0])
gamma = [most_common_val(report, i) for i in range(h_size)]
epsilon = [0 if dig else 1 for dig in gamma]

oxygen = co2 = report
for i in range(h_size):
	oxygen = [line for line in oxygen if line[i] == most_common_val(oxygen, i)]
	co2 = [line for line in co2 if line[i] != most_common_val(co2, i)] if len(co2) > 1 else co2

print(f"Part 1: {bin_array_to_int(gamma) * bin_array_to_int(epsilon)}")
print(f"Part 2: {bin_array_to_int(oxygen[0]) * bin_array_to_int(co2[0])}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
