import time
import networkx

begin = time.time()

###

def neighbour_can_be_visited(neighbour: str, path: list, special_small_cave: str) -> bool:
	if neighbour[0].isupper():
		return True
	if neighbour not in path:
		return True
	if neighbour == special_small_cave and path.count(neighbour) < 2:
		return True
	return False

def get_all_paths(graph, special_small_cave: str) -> set:
	finished_paths = set()
	unfinished_paths = [["start"]]
	while unfinished_paths:
		tmp = []
		for path in unfinished_paths:
			last_visited_cave = path[-1]
			if last_visited_cave == "end":
				path_as_str = ",".join(path)
				finished_paths.add(path_as_str)
				continue
			for neighbour in graph.neighbors(last_visited_cave):
				if neighbour_can_be_visited(neighbour, path, special_small_cave):
					tmp.append(path + [neighbour])
		unfinished_paths = tmp
	return finished_paths


cave_graph = networkx.Graph()
with open("input.txt") as file:
	for line in file:
		cave_a, cave_b = line.strip().split("-")
		cave_graph.add_edge(cave_a, cave_b)

small_caves = [cave for cave in cave_graph.nodes()
				if cave[0].islower()
				and cave not in ["start", "end"]]

p1_paths = get_all_paths(cave_graph, None)
p2_paths = set().union(*[get_all_paths(cave_graph, cave) for cave in small_caves])

print(f"Part 1: {len(p1_paths)}")
print(f"Part 2: {len(p2_paths)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
