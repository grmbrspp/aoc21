import time
import heapq
from functools import cache

begin = time.time()

###

HALLWAY = "..!.!.!.!.."
EXIT_INDIZES = {char: 2 + 2*idx for idx, char in enumerate("ABCD")}
HOMES = [
	{
		char: [2*(idx+1) - (n+1) for n in range(2)]
		for idx, char in enumerate("ABCD")
	},
	{
		char: [4*(idx+1) - (n+1) for n in range(4)]
		for idx, char in enumerate("ABCD")
	}
]
FINISHED_ROOMS = [
	"".join(char*2 for char in "ABCD"),
	"".join(char*4 for char in "ABCD"),
]
ENERGY_PER_STEP = {char: 10**idx for idx, char in enumerate("ABCD")}


@cache
def cost_fn(ridx: int, room_size: int, hidx: int, cost_per_step: int) -> int:
	way_out = ridx % room_size + 1
	hallway_dist = abs(2 + 2*ridx // room_size - hidx)
	return (way_out + hallway_dist) * cost_per_step

def free_hallway_spots(ridx: int, room_size: int, h: str):
	exit_idx = 2 + 2*ridx // room_size
	left_of_exit = range(exit_idx,-1,-1)
	right_of_exit = range(exit_idx,len(h))
	for positions in (left_of_exit, right_of_exit):
		for p_idx in positions:
			if h[p_idx] == ".":
				yield p_idx
				continue
			if h[p_idx] in "ABCD":
				break

@cache
def movable_animals(r: str) -> list:
	result = []
	room_size = len(r) // 4
	rooms = [r[i*room_size:i*room_size+room_size] for i in range(4)]
	for r_num, room in enumerate(rooms):
		if all(char in "ABCD"[r_num] + "." for char in room):
			continue
		for idx, animal in enumerate(room):
			if animal == ".":
				continue
			ridx = idx + r_num*room_size
			result.append((ridx, animal))
			break
	return result

@cache
def possible_moves(r: str, h: str) -> list:
	room_size = len(r) // 4
	# MOVE HOME
	for hidx, animal in enumerate(h):
		if animal not in "ABCD":
			continue
		exit_idx = EXIT_INDIZES[animal]
		way = h[hidx+1:exit_idx] if exit_idx > hidx else h[exit_idx:hidx]
		if any(char in way for char in "ABCD"):
			continue
		for ridx in HOMES[room_size == 4][animal]:
			if r[ridx] == animal:
				continue
			if r[ridx] == ".":
				new_r = "".join(char if idx != ridx else animal for idx, char in enumerate(r))
				new_h = "".join(char if idx != hidx else "." for idx, char in enumerate(h))
				cost_per_step = ENERGY_PER_STEP[animal]
				return [(new_r, new_h, cost_fn(ridx, room_size, hidx, cost_per_step))]
			break
	# MOVE TO HALLWAY
	result = []
	for ridx, animal in movable_animals(r):
		cost_per_step = ENERGY_PER_STEP[animal]
		for hidx in free_hallway_spots(ridx, room_size, h):
			new_r = "".join(char if idx != ridx else "." for idx, char in enumerate(r))
			new_h = "".join(char if idx != hidx else animal for idx, char in enumerate(h))
			result.append((new_r, new_h, cost_fn(ridx, room_size, hidx, cost_per_step)))
	return result

def dijkstra_shortest_path(start_rooms: str, finish: str) -> int:
	queue = []
	heapq.heappush(queue, (0, (start_rooms, HALLWAY)))
	visited = set()
	while queue:
		cost, state = heapq.heappop(queue)
		if state in visited:
			continue
		if state[0] == finish:
			return cost
		visited.add(state)
		for r, h, move_cost in possible_moves(*state):
			if (r,h) in visited:
				continue
			heapq.heappush(queue, (cost+move_cost, (r, h)))
	return float("inf")


with open("input.txt") as file:
	chars = [char for char in file.read() if char in "ABCD"]

p1_rooms = "".join(chars[0+i] + chars[12+i] for i in range(4))
p2_rooms = "".join(
	"".join(chars[(0+i+(j*4))] for j in range(4))
	for i in range(4)
)

print(f"Part 1: {dijkstra_shortest_path(p1_rooms, FINISHED_ROOMS[0])}")
print(f"Part 2: {dijkstra_shortest_path(p2_rooms, FINISHED_ROOMS[1])}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
