import time
from functools import cache
from itertools import chain

begin = time.time()

###

HALLWAY = "..0.1.2.3.."
EXIT_INDIZES = [2,4,6,8]
HOMES = [
	{
		"A": [1,0],
		"B": [3,2],
		"C": [5,4],
		"D": [7,6],
	},
	{
		"A": [3,2,1,0],
		"B": [7,6,5,4],
		"C": [11,10,9,8],
		"D": [15,14,13,12],
	}
]
ENERGY_PER_STEP = {
	"A": 1,
	"B": 10,
	"C": 100,
	"D": 1000
}

@cache
def finished_rooms(room_size: int) -> str:
	return "".join(char*room_size for char in "ABCD")

@cache
def free_hallway_spots(ridx: int, room_size: int, h: str) -> list:
	result = []
	exit_idx = EXIT_INDIZES[ridx // room_size]
	left_of_exit = range(exit_idx,-1,-1)
	right_of_exit = range(exit_idx,len(h))
	for positions in (left_of_exit, right_of_exit):
		for p_idx in positions:
			if h[p_idx] == ".":
				result.append(p_idx)
				continue
			if str(h[p_idx]) in "ABCD":
				break
	return result

@cache
def cost_fn(ridx: int, room_size: int, hidx: int, animal: str) -> int:
	way_out = ridx % room_size + 1
	hallway_dist = abs(EXIT_INDIZES[ridx // room_size] - hidx)
	return (way_out + hallway_dist) * ENERGY_PER_STEP[animal]

@cache
def movable_animals(r: str) -> list:
	result = []
	room_size = len(r) // 4
	for ridx, animal in enumerate(r):
		if ridx % room_size == 0:
			skip_room = False
			room = r[ridx:ridx + room_size]
			others_in_room = [char for char in room
								if char not in [finished_rooms(room_size)[ridx], "."]]
			if not others_in_room:
				skip_room = True
		if skip_room:
			continue
		if animal == ".":
			continue
		result.append((ridx, animal))
		skip_room = True
	return result

@cache
def possible_moves(r: str, h: str) -> list:
	room_size = len(r) // 4
	# MOVE HOME
	for hidx, animal in enumerate(h):
		if animal not in "ABCD":
			continue
		exit_idx = EXIT_INDIZES[HOMES[room_size == 4][animal][0] // room_size]
		way = h[hidx+1:exit_idx] if exit_idx > hidx else h[exit_idx:hidx]
		if any(char in way for char in "ABCD"):
			continue
		for ridx in HOMES[room_size == 4][animal]:
			if r[ridx] == animal:
				continue
			if r[ridx] == ".":
				new_r = "".join(char if idx != ridx else animal for idx, char in enumerate(r))
				new_h = "".join(char if idx != hidx else "." for idx, char in enumerate(h))
				return [(new_r, new_h, cost_fn(ridx, room_size, hidx, animal))]
			break
	# MOVE TO HALLWAY
	result = []
	for ridx, animal in movable_animals(r):
		for hidx in free_hallway_spots(ridx, room_size, h):
			new_r = "".join(char if idx != ridx else "." for idx, char in enumerate(r))
			new_h = "".join(char if idx != hidx else animal for idx, char in enumerate(h))
			result.append((new_r, new_h, cost_fn(ridx, room_size, hidx, animal)))
	return result

@cache
def find_lowest_cost(r: str, h: str, cost: int, best=float("inf")) -> int:
	if cost > best:
		return cost
	if r == finished_rooms(len(r) // 4):
		return cost
	for move in possible_moves(r,h):
		this_cost = cost + find_lowest_cost(*move, best)
		if this_cost < best:
			best = this_cost
	return best


with open("input.txt") as file:
	chars = [char for char in file.read() if char in "ABCD"]

p1_rooms = chars[0] + chars[12] +\
			chars[1] + chars[13] +\
			chars[2] + chars[14] +\
			chars[3] + chars[15]

p2_rooms = chars[0] + chars[4] + chars[8] + chars[12] +\
			chars[1] + chars[5] + chars[9] + chars[13] +\
			chars[2] + chars[6] + chars[10] + chars[14] +\
			chars[3] + chars[7] + chars[11] + chars[15]

print(f"Part 1: {find_lowest_cost(p1_rooms, HALLWAY, 0)}")
print(f"Part 2: {find_lowest_cost(p2_rooms, HALLWAY, 0)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
