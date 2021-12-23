import time
import math
from collections import defaultdict
import itertools

begin = time.time()

###

def cube_orientations(i: int, x: int, y: int, z: int) -> tuple: 
	return [
		(x,y,z), (y,-x,z), (-x,-y,z), (-y,x,z),
		(z,y,-x), (z,-x,-y), (z,-y,x), (z,x,y),
		(x,z,-y), (-y,z,-x), (-x,z,y), (y,z,x),
		(-x,y,-z), (y,x,-z), (x,-y,-z), (-y,-x,-z),
		(-z,y,x), (-z,x,-y), (-z,-y,-x), (-z,-x,-y),
		(-x,-z,-y), (-y,-z,x), (x,-z,y), (y,-z,-x)
	][i]

def distance(p: tuple, q: tuple) -> float:
	dist = math.sqrt(sum( (p_i - q_i)**2 for p_i, q_i in zip(p,q)))
	return round(dist, 3)

def manhattan_distance(p: tuple, q: tuple) -> int:
	return sum(abs(p_i - q_i) for p_i, q_i in zip(p,q))


class Scanner:
	def __init__(self):
		self.detected_beacons = []
		self.known_scanner_positions = [(0,0,0)]
		self.inter_beacon_distances = defaultdict(set)

	def get_orientations(self):
		for i in range(24):
			yield [cube_orientations(i, *b) for b in self.detected_beacons]

	def calculate_inter_beacon_distances(self):
		self.inter_beacon_distances.clear()
		for i, a in enumerate(self.detected_beacons):
			for b in self.detected_beacons[i+1:]:
				dist = distance(a,b)
				self.inter_beacon_distances[a].add(dist)
				self.inter_beacon_distances[b].add(dist)

	def find_beacon(self, other_dists) -> bool:
		for own_beacon, own_dists in self.inter_beacon_distances.items():
			if len(own_dists & other_dists) > 10:
				return own_beacon
		return None

	def find_overlaping_beacons(self, other):
		overlap = []
		for other_beacon, disctances in other.inter_beacon_distances.items():
			match = s.find_beacon(disctances)
			if match is not None:
				overlap.append((match, other_beacon))
		return overlap

	def extend(self, other, overlap):
		overlap_indizes = [other.detected_beacons.index(match[1]) for match in overlap]
		for o_idx, orientation in enumerate(other.get_orientations()):
			diffs_between_matches = set()
			for m_idx, match in enumerate(overlap):
				a, b = match[0], orientation[overlap_indizes[m_idx]]
				diffs_between_matches.add(tuple(p-q for p,q in zip(a,b)))
			correct_orientation_found = len(diffs_between_matches) == 1
			if not correct_orientation_found:
				continue
			scanner_position = diffs_between_matches.pop()
			new_beacons = [tuple(p+q for p,q in zip(beacon, scanner_position))
							for beacon in orientation]
			self.detected_beacons.extend(b for b in new_beacons if b not in self.detected_beacons)
			self.known_scanner_positions.extend(
				[tuple(p+q for p,q in zip(scanner_position, cube_orientations(o_idx, *s)))
					for s in other.known_scanner_positions]
			)
			break
		self.calculate_inter_beacon_distances()

	def try_extend(self, other) -> bool:
		overlap = self.find_overlaping_beacons(other)
		if len(overlap) < 12:
			return False
		s.extend(other, overlap)
		return True


scanners = []
with open("input.txt") as file:
	for line in file:
		if not line.strip():
			continue
		if "scanner" in line:
			scanners.append(Scanner())
			continue
		scanners[-1].detected_beacons.append(tuple(int(n) for n in line.strip().split(",")))

for s in scanners:
	s.calculate_inter_beacon_distances()

full_map = Scanner()
scanner_to_be_added = set(scanners)
while len(full_map.known_scanner_positions) < len(scanners):
	for s, t in itertools.permutations(scanners, 2):
		if s not in scanner_to_be_added or t not in scanner_to_be_added:
			continue
		if s.try_extend(t):
			scanner_to_be_added.remove(t)
			full_map = s

distances_between_scanners = [manhattan_distance(s,t)
								for s in full_map.known_scanner_positions
								for t in full_map.known_scanner_positions]

print(f"Part 1: {len(full_map.detected_beacons)}")
print(f"Part 2: {max(distances_between_scanners)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
