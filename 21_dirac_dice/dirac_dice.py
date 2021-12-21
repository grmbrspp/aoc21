import time
from collections import Counter
from functools import cache

begin = time.time()

###

QUANTUM_DIE = Counter(
	[d1+d2+d3
		for d1 in [1,2,3]
		for d2 in [1,2,3]
		for d3 in [1,2,3]
	]
).items()

def deterministic_die(sides_count: int) -> tuple:
	turn = 0
	while True:
		yield (turn % sides_count + 1, turn)
		turn += 1

def play_deterministic(start_pos) -> int:
	positions = list(start_pos)
	scores = [0 for player in start_pos]
	die = deterministic_die(100)
	player = -1
	while scores[player] < 1000:
		player = (player+1) % 2
		throw = sum(next(die)[0] for _ in range(3))
		new_pos = (positions[player] + throw) % 10
		positions[player] = 10 if new_pos == 0 else new_pos
		scores[player] += positions[player]
	return min(scores) * next(die)[1]

@cache
def get_win_counts(positions, scores=(0,0)):
	p0_win_count, p1_win_count = 0, 0
	for throw, throw_count in QUANTUM_DIE:
		new_pos = (positions[0] + throw) % 10
		new_pos = 10 if new_pos == 0 else new_pos
		new_score = scores[0] + new_pos
		if new_score >= 21:
			p0_win_count += throw_count
			continue
		p1_sub_count, p0_sub_count = get_win_counts((positions[1], new_pos), (scores[1], new_score))
		p0_win_count += p0_sub_count * throw_count
		p1_win_count += p1_sub_count * throw_count
	return (p0_win_count, p1_win_count)


with open("input.txt") as file:
	start_positions = tuple(int(line.split()[-1]) for line in file)

print(f"Part 1: {play_deterministic(start_positions)}")
print(f"Part 2: {max(get_win_counts(start_positions))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
