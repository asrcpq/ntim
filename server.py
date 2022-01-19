import os
import socket
import pickle
import itertools

print("Loading files")
with open("ngrams.pkl", "rb") as f:
	ngrams = pickle.load(f)
bigram_n1 = sum([1 for i in ngrams[2].values() if i == 1 ])
unigram_sum = sum(ngrams[1].values())
print(f"bigram n1: {bigram_n1}, unigram sum: {unigram_sum}")

mapper_l2c = {}
mapper_c2l = {}
with open(os.environ['NTIM_MAPPER'], "r") as f:
	for line in f:
		(lat, ch) = line.split()
		if lat in mapper_l2c:
			mapper_l2c[lat].append(ch)
		else:
			mapper_l2c[lat] = [ch]
		if ch in mapper_c2l:
			mapper_c2l[ch].append(lat)
		else:
			mapper_c2l[ch] = [lat]

input_mapper = {}
bad = 0; good = 0
print("Generating input mapper")
for ngram in ngrams:
	for key in ngram.keys():
		lat = []
		flag = True
		for k in key:
			if k in mapper_c2l:
				lat.append(mapper_c2l[k])
			else:
				flag = False
				break
		if not flag:
			if key[0] != 's':
				bad += 1
			continue
		good += 1
		for lat in ["".join(tup) for tup in itertools.product(*lat)]:
			if lat in input_mapper:
				input_mapper[lat].append(key)
			else:
				input_mapper[lat] = [key]

print(f"ready with g:{good} b:{bad}")

def bigram_query(prefix: str, ch1: str) -> float:
	dict1 = ngrams[2]
	str_all = prefix + ch1
	# laplace smoothing
	if str_all not in dict1:
		result = bigram_n1 * ngrams[1][ch1] / unigram_sum
	else:
		c1 = dict1[str_all]
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
			count = ngrams[len(candidate)][candidate]
			if len(candidate) == 1:
				count2 = count
			else:
				count2 = ngrams[len(candidate) - 1][candidate[:-1]]
			weights[idx] = prob * count / count2
			#print(prob, candidate, count)
	#print(list(zip(candidates, weights)))
	candidates_sorted = [x for x, _ in sorted(
		zip(candidates, weights),
		key = lambda tup: tup[1],
		reverse = True,
	)]
	return candidates_sorted

socket = socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM)
socket_path = "ntim.socket"
socket.bind(socket_path)
socket.listen(1)
try:
	while True:
		connection, address = socket.accept()
		print("connected from", address)
		while True:
			data = connection.recv(1024)
			print("recv: ", data)
			if not data:
				break
			decoded = data.decode('utf-8').strip()
			input_buffer, buffer = decoded.split(" ", 1)
			candidates = get_candidates(input_buffer)
			print("send: ", candidates)
			connection.send(pickle.dumps(candidates))
finally:
	socket.close()
	os.remove(socket_path)