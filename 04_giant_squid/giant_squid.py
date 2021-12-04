import time

begin = time.time()

###

def is_solved(rows: list, drawn_nums: set) -> bool:
	for row in rows:
		if all(n in drawn_nums for n in row):
			return True
	return False

def get_score(bingo_board: list, drawn_nums: set, last_draw: int) -> int:
	unmarked_numbers = [n for n in bingo_board if n not in drawn_nums]
	return sum(unmarked_numbers) * last_draw


with open("input.txt") as file:
	file_sections = file.read().split("\n\n")
	draws = [int(n) for n in file_sections.pop(0).strip().split(",")]
	boards = [[int(n) for n in section.strip().split()] for section in file_sections]

rows_and_cols = {}
for b_idx, board in enumerate(boards):
	board_rows = [board[i:i+5] for i in range(0, 5*5, 5)]
	board_cols = [board[i::5] for i in range(5)]
	rows_and_cols[b_idx] = board_rows + board_cols

drawn, solved = set(), set()
scores = []
for d_idx, draw in enumerate(draws):
	drawn.add(draw)
	for b_idx, board in enumerate(boards):
		if b_idx not in solved and is_solved(rows_and_cols[b_idx], drawn):
			solved.add(b_idx)
			scores.append(get_score(board, drawn, draw))

print(f"Part 1: {scores[0]}")
print(f"Part 2: {scores[-1]}")

###

end = time.time()
print(f"Runtime: {end - begin}")
