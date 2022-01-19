import sys
import pickle

ngrams = [{}]
lines = []
for line in sys.stdin:
	lines.append(line)
for n in range(1, 3):
	print(f"Processing {n}-gram")
	ngram = {}

	line_num = len(lines)
	for (idx, line) in enumerate(lines):
		if idx % (line_num // 10) == 0:
			print(f"{idx}/{line_num}")
		line = f"s{line.strip()}" # s is start of seq
		if len(line) <= n - 1:
			continue
		for i in range(len(line) - n):
			key = line[i:i+n]
			if key in ngram:
				ngram[key] += 1
			else:
				ngram[key] = 1
	ngrams.append(ngram)

with open('ngrams.pkl', 'wb') as file:
	pickle.dump(ngrams, file)