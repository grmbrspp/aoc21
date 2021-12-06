import time
from collections import deque

begin = time.time()

###

def fish_count_after_n_gens(init_state: list, n: int) -> int:
	q = deque(init_state.count(i) for i in range(9))
	for _ in range(n):
		q[-2] += q[0]
		q.rotate(-1)
	return sum(q)


with open("input.txt") as file:
	fish_timers = [int(n) for n in file.read().strip().split(",")]

print(f"Part 1: {fish_count_after_n_gens(fish_timers, 80)}")
print(f"Part 1: {fish_count_after_n_gens(fish_timers, 256)}")

###

end = time.time()
print(f"Runtime: {end - begin}")
