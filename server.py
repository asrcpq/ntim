import os
import socket
import pickle
import itertools
import var

print("Loading files")
with open("ntim.pkl", "rb") as f:
	ntim_data = pickle.load(f)
ngrams = ntim_data.ngrams
bigram_n1 = ntim_data.bigram_n1
unigram_sum = ntim_data.unigram_sum
print(f"bigram n1: {bigram_n1}, unigram sum: {unigram_sum}")

input_mapper = {}
bad = 0; good = 0
for ngram in ngrams:
	for (key, value) in ngram.items():
		for lat in value[0]:
			if lat in input_mapper:
				input_mapper[lat].append(key)
			else:
				input_mapper[lat] = [key]

def bigram_query(prefix: str, ch1: str) -> float:
	dict1 = ngrams[2]
	str_all = prefix + ch1
	# laplace smoothing
	if str_all not in dict1:
		result = bigram_n1 * ngrams[1][ch1][1] / unigram_sum
	else:
		c1 = dict1[str_all][1]
		result = c1
	#print(prefix, ch1, result)
	return result

def get_candidates(input_buffer):
	if input_buffer not in input_mapper:
		return []
	candidates = input_mapper[input_buffer]
	queries = {} # map first char to candidate indices
	for (idx, candidate) in enumerate(candidates):
		ch1 = candidate[0]
		if ch1 in queries:
			queries[ch1].append(idx)
		else:
			queries[ch1] = [idx]
	weights = [0.0 for _ in candidates]
	for ch1 in queries.keys():
		prob = bigram_query(buffer[-1], ch1)
		for idx in queries[ch1]:
			candidate = candidates[idx]
			count = ngrams[len(candidate)][candidate][1]
			if len(candidate) == 1:
				count2 = count
			else:
				count2 = ngrams[len(candidate) - 1][candidate[:-1]][1]
			weights[idx] = prob * count / count2
			#print(prob, candidate, count)
	#print(list(zip(candidates, weights)))
	candidates_sorted = [x for x, _ in sorted(
		zip(candidates, weights),
		key = lambda tup: tup[1],
		reverse = True,
	)]
	candidates = []
	total_len = 0
	for candidate in candidates_sorted:
		total_len += len(candidate)
		if total_len >= var.candidate_len:
			break
		candidates.append(candidate)
	return candidates

socket = socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM)
socket_path = "ntim.socket"
socket.bind(socket_path)
socket.listen(1)
try:
	while True:
		connection, address = socket.accept()
		print("connected from", address)
		while True:
			data = connection.recv(var.msg_len)
			#print("recv: ", data)
			if not data:
				break
			decoded = data.decode('utf-8').strip()
			input_buffer, buffer = decoded.split(" ", 1)
			candidates = get_candidates(input_buffer)
			#print("send: ", candidates)
			connection.send(pickle.dumps(candidates))
finally:
	socket.close()
	os.remove(socket_path)
