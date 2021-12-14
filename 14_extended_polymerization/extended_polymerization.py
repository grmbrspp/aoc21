import time
from collections import Counter

begin = time.time()

###

def element_count_after_n_steps(n: int) -> list:
	pair_counter = Counter({
		pair: TEMPLATE.count(pair)
		for pair in INSERTION_RULES
		if pair in TEMPLATE
	})
	element_counter = Counter(TEMPLATE)
	for _ in range(n):
		for pair, count in list(pair_counter.items()):
			elem_a, elem_b = list(pair)
			new_elem = INSERTION_RULES[elem_a+elem_b]
			element_counter[new_elem] += count
			pair_counter[elem_a+new_elem] += count
			pair_counter[new_elem+elem_b] += count
			pair_counter[pair] -= count
	return element_counter.most_common()


TEMPLATE = ""
INSERTION_RULES = {}
with open("input.txt") as file:
	for line in file:
		if "->" in line:
			a, b = line.strip().split(" -> ")
			INSERTION_RULES[a] = b
		elif line.strip():
			TEMPLATE = line.strip()

p1_element_counts = element_count_after_n_steps(10)
p2_element_counts = element_count_after_n_steps(40)

print(f"Part 1: {p1_element_counts[0][1] - p1_element_counts[-1][1]}")
print(f"Part 2: {p2_element_counts[0][1] - p2_element_counts[-1][1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
