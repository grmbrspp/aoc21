import time
import heapq

begin = time.time()

###

def extend_on_axis(axis: str, risk_map: dict) -> dict:
	result = {}
	grid_size = max(risk_map)[0]+1 if axis == "x" else max(risk_map)[1]+1
	risk_map_items = list(risk_map.items())
	for i in range(5):
		delta = (i*grid_size, 0) if axis == "x" else (0, i*grid_size)
		for point, risk in risk_map_items:
			new_point = (point[0] + delta[0], point[1] + delta[1])
			new_risk = risk + i
			result[new_point] = new_risk if new_risk < 10 else new_risk - 9
	return result

def extend_risk_map(risk_map: dict):
	x_extension = extend_on_axis("x", risk_map)
	return extend_on_axis("y", x_extension)

def get_neighbours(point: tuple):
	for dx, dy in [(0,1), (1,0), (-1,0), (0,-1)]:
		neighbour = (point[0] + dx, point[1] + dy)
		yield neighbour

def dijkstra(start: tuple, finish: tuple, risk_map: dict) -> int:
	queue = []
	heapq.heappush(queue, (0, start))
	visited = set()
	while queue:
		dist, point = heapq.heappop(queue)
		if point == finish:
			return dist
		if point in visited:
			continue
		visited.add(point)
		for neighbour in get_neighbours(point):
			neighbour_risk = risk_map.get(neighbour, -1)
			if neighbour_risk > 0:
				heapq.heappush(queue, (dist + neighbour_risk, neighbour))


risk_map_p1 = {}
with open("input.txt") as file:
	for y, line in enumerate(file):
		for x, height in enumerate(line.strip()):
			risk_map_p1[(x,y)] = int(height)
			bottom_right_p1 = (x,y)

risk_map_p2 = extend_risk_map(risk_map_p1)
top_left = (0,0)
bottom_right_p1 = max(risk_map_p1)
bottom_right_p2 = max(risk_map_p2)

print(f"Part 1: {dijkstra(top_left, bottom_right_p1, risk_map_p1)}")
print(f"Part 2: {dijkstra(top_left, bottom_right_p2, risk_map_p2)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
