import time

begin = time.time()

###

def get_rows(l: list) -> list:
	return [l[i:i+5] for i in range(0, 25, 5)]

def get_cols(l: list) -> list:
	return [l[i::5] for i in range(5)]

def is_solved(b: list, drawn_nums: set):
	for line in get_rows(b) + get_cols(b):
			if all(n in drawn_nums for n in line):
				return True
	return False

boards = []
with open("input.txt") as file:
	file_sections = file.read().split("\n\n")
	draws = [int(n) for n in file_sections.pop(0).strip().split(",")]
	boards = [[int(n) for n in section.strip().split()] for section in file_sections]

drawn, solved = set(), {}
for d_idx, draw in enumerate(draws):
	drawn.add(draw)
	for b_idx, board in enumerate(boards):
		if b_idx not in solved and is_solved(board, drawn):
			solved[b_idx] = d_idx

unmarked_numbers = lambda board, draw: [n for n in boards[board] if n not in draws[:draw+1]]
score = lambda board, draw: sum(unmarked_numbers(board, draw)) * draws[draw]

ranking = sorted(solved.items(), key=lambda kvp: kvp[1])
winner_idx, winner_draw_idx = ranking[0]
looser_idx, looser_draw_idx = ranking[-1]

print(f"Part 1: {score(winner_idx, winner_draw_idx)}")
print(f"Part 2: {score(looser_idx, looser_draw_idx)}")

###

end = time.time()
print(f"Runtime: {end - begin}")
