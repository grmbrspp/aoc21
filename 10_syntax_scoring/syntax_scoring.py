import time
from collections import deque

begin = time.time()

###

def get_line_state(line: str) -> tuple:
	stack = deque()
	bracket_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
	for char in line:
		if char in bracket_pairs:
			stack.append(bracket_pairs[char])
			continue
		if char != stack.pop():
			return ("corrupted", char)
	missing_chars = "".join(reversed(stack))
	return ("incomplete", missing_chars)

def get_syntax_score(char: str) -> int:
	score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
	return score_table[char]

def get_autocomplete_score(completion: str) -> int:
	score = 0
	score_table = {")": 1, "]": 2, "}": 3, ">": 4}
	for char in completion:
		score = 5 * score + score_table[char]
	return score


with open("input.txt") as file:
		line_states = [get_line_state(line.strip()) for line in file]

corrupted_lines = [state for state in line_states if state[0] == "corrupted"]
incomplete_lines = [state for state in line_states if state[0] == "incomplete"]

syntax_scores = [get_syntax_score(state[1]) for state in corrupted_lines]
autocomplete_scores = [get_autocomplete_score(state[1]) for state in incomplete_lines]
autocomplete_scores.sort()
winner_index = len(autocomplete_scores)//2

print(f"Part 1: {sum(syntax_scores)}")
print(f"Part 2: {autocomplete_scores[winner_index]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
