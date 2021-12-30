import time
from collections import defaultdict
from functools import cache

begin = time.time()

###

@cache
def get_neighbours(pixel: tuple):
	neighbours = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
	return [(pixel[0] + dx, pixel[1] + dy) for dx, dy in neighbours]

def enhance(img: dict, size: tuple, a: list, iteration: int) -> dict:
	result = defaultdict(lambda: a[0] if iteration % 2 == 0 else 0)
	min_x, max_x, min_y, max_y = size
	for x in range(min_x, max_x+1):
		for y in range(min_y, max_y+1):
			binary = "".join(str(img[n]) for n in get_neighbours((x,y)))
			result[(x,y)] = a[int(binary, 2)]
	return result


with open("input.txt") as file:
	sections = file.read().split("\n\n")

algorithm = [int(char == "#") for char in sections[0].strip()]
image = defaultdict(int)
for y_coord, line in enumerate(sections[1].split("\n")):
	for x_coord, char in enumerate(line):
		image[(x_coord,y_coord)] = int(char == "#")
image_dimensions = (
	0, max(image)[0],
	0, max(image, key=lambda p: p[1])[1]
)

images = [image]
for i in range(50):
	image_dimensions = (
		image_dimensions[0]-1, image_dimensions[1]+1,
		image_dimensions[2]-1, image_dimensions[3]+1
	)
	images.append(enhance(images[-1], image_dimensions, algorithm, i))

print(f"Part 1: {sum(images[2].values())}")
print(f"Part 2: {sum(images[-1].values())}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
