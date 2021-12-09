import time
import statistics

begin = time.time()

###

def gauss_dist(n: int) -> int:
	return int(n*(n+1)/2)

def get_dist(points: list, p: int, constant_rate: bool) -> int:
	if constant_rate:
		return sum([abs(p-q) for q in points])
	return sum([gauss_dist(abs(p-q)) for q in points])

def get_min_dist_mean(points: list, p: int, constant_rate: bool) -> int:
	dists = {name: \
		get_dist(points, q, constant_rate) \
		for name, q in [("this", p), ("lower", p-1), ("upper", p+1)] \
	}

	if min(dists.values()) == dists["this"]:
		return p

	p = p-1 if dists["lower"] < dists["upper"] else p+1
	return get_min_dist_mean(points, p, constant_rate)


with open("input.txt") as file:
	crab_positions = [int(n) for n in file.read().strip().split(",")]

p1_mean = round(statistics.median(crab_positions))
start_point = statistics.mean(crab_positions)
p2_mean = get_min_dist_mean(crab_positions, start_point, False)

print(f"Part 1: {get_dist(crab_positions, p1_mean, True)}")
print(f"Part 2 {get_dist(crab_positions, p2_mean, False)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
