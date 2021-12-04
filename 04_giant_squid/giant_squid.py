import time

begin = time.time()

###

def is_solved(rows: list, drawn_nums: set) -> bool:
	for row in rows:
			if all(n in drawn_nums for n in row):
				return True
	return False

def get_score(bingo_board: list, drawn_nums: list) -> int:
	unmarked_numbers = [n for n in bingo_board if n not in drawn_nums]
	return sum(unmarked_numbers) * drawn_nums[-1]


with open("input.txt") as file:
	file_sections = file.read().split("\n\n")
	draws = [int(n) for n in file_sections.pop(0).strip().split(",")]
	boards = [[int(n) for n in section.strip().split()] for section in file_sections]

rows_and_cols = {}
for b_idx, board in enumerate(boards):
	board_rows = [board[i:i+5] for i in range(0, 5*5, 5)]
	board_cols = [board[i::5] for i in range(5)]
	rows_and_cols[b_idx] = board_rows + board_cols

drawn, solved = set(), {}
for d_idx, draw in enumerate(draws):
	drawn.add(draw)
	for b_idx, board in enumerate(boards):
		if b_idx not in solved and is_solved(rows_and_cols[b_idx], drawn):
			solved[b_idx] = d_idx

ranking = sorted(solved.items(), key=lambda kvp: kvp[1])

winner_idx, winner_draw_idx = ranking[0]
winner_score = get_score(boards[winner_idx], draws[:winner_draw_idx+1])

looser_idx, looser_draw_idx = ranking[-1]
looser_score = get_score(boards[looser_idx], draws[:looser_draw_idx+1])

print(f"Part 1: {winner_score}")
print(f"Part 2: {looser_score}")

###

end = time.time()
print(f"Runtime: {end - begin}")
