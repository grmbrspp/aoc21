import time
from collections import namedtuple

begin = time.time()

###

HEX_TO_BIN = {
	"0": "0000",
	"1": "0001",
	"2": "0010",
	"3": "0011",
	"4": "0100",
	"5": "0101",
	"6": "0110",
	"7": "0111",
	"8": "1000",
	"9": "1001",
	"A": "1010",
	"B": "1011",
	"C": "1100",
	"D": "1101",
	"E": "1110",
	"F": "1111",
}

Packet = namedtuple("Packet", ["version", "type", "sub_count", "value"])


def product(iteralbe) -> int:
	acc = 1
	for n in iteralbe:
		acc *= n
	return acc

def read_literal(bin_str: str) -> tuple:
	bin_number = ""
	i = 0
	while True:
		bin_number += bin_str[i+1:i+5]
		if bin_str[i] == "0":
			break
		i += 5
	return (int(bin_number, 2), bin_str[i+5:])

def read_packets(bin_str: str) -> list:
	result = []
	if "1" not in bin_str:
		return result
	version = int(bin_str[:3], 2)
	type_id = int(bin_str[3:6], 2)
	match type_id, bin_str[6] == "0":
		case 4,_:
			value, remainder = read_literal(bin_str[6:])
			result.append(Packet(version, type_id, 0, value))
		case _,True:
			length = int(bin_str[7:7+15], 2)
			sub_packets = read_packets(bin_str[7+15:7+15+length])
			sub_count = len(sub_packets) - sum(p.sub_count for p in sub_packets)
			result.append(Packet(version, type_id, sub_count, 0))
			result.extend(sub_packets)
			remainder = bin_str[7+15+length:]
		case _,False:
			length = int(bin_str[7:7+11], 2)
			result.append(Packet(version, type_id, length, 0))
			remainder = bin_str[7+11:]
	result.extend(read_packets(remainder))
	return result

def evaluate_next_packet(packets: list) -> int:
	packet = packets.pop(0)
	match packet.type:
		case 0:
			return sum(evaluate_next_packet(packets) for i in range(packet.sub_count))
		case 1:
			return product(evaluate_next_packet(packets) for i in range(packet.sub_count))
		case 2:
			return min(evaluate_next_packet(packets) for i in range(packet.sub_count))
		case 3:
			return max(evaluate_next_packet(packets) for i in range(packet.sub_count))
		case 4:
			return packet.value
		case 5:
			return int(evaluate_next_packet(packets) > evaluate_next_packet(packets))
		case 6:
			return int(evaluate_next_packet(packets) < evaluate_next_packet(packets))
		case 7:
			return int(evaluate_next_packet(packets) == evaluate_next_packet(packets))


with open("input.txt") as file:
	input_hex = file.read().strip()

input_bin = ""
for hex_digit in input_hex:
	input_bin += HEX_TO_BIN[hex_digit]

packet_list = read_packets(input_bin)

print(f"Part 1: {sum(p.version for p in packet_list)}")
print(f"Part 2: {evaluate_next_packet(packet_list)}")



###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
