# Read evaluated corpus from stdin
# each line, word to input should be split by space

import sys
import pickle
import ntim
from collections import Counter

ngrams = ntim.ngrams
input_mapper = ntim.input_mapper
rec_ranks = []
recsum = 0
hit = 0
rec_ranks2 = []
recsum2 = 0
hit2 = 0
count = 0

for (idx, line) in enumerate(sys.stdin):
	if idx % 100 == 0:
		print(idx, file = sys.stderr)
	segs = line.split()
	for (i, seg) in enumerate(segs):
		count += 1
		rec_ranks.append(0)
		rec_ranks2.append(0)
		try:
			spell = ngrams[len(seg)][seg][0][0] # use first candidates only
		except KeyError:
			continue
		except IndexError:
			continue

		# simple freq
		rec_rank = 0
		try:
			candidates = input_mapper[spell]
			cand_counts = [ngrams[len(candidate)][candidate][1] for candidate in candidates]
		except KeyError:
			pass
		except IndexError:
			pass
		candidates_sorted = [x for x, _ in sorted(
			zip(candidates, cand_counts),
			key = lambda tup: tup[1],
			reverse = True,
		)]
		for (idx, candidate_in_count_order) in enumerate(candidates_sorted):
			if seg == candidate_in_count_order:
				rec_rank = 1 / (1 + idx)
				rec_ranks[-1] = rec_rank
				if idx < 5:
					hit += 1
				break
		recsum += rec_rank

		# ngram prediction
		rec_rank = 0
		if i == 0:
			buf = 's'
		else:
			buf = segs[i - 1][-1]
		candidates_sorted = ntim.get_candidates(spell, buf)
		for (idx, candidate_in_count_order) in enumerate(candidates_sorted):
			if seg == candidate_in_count_order:
				rec_rank = 1 / (1 + idx)
				rec_ranks2[-1] = rec_rank
				if idx < 5:
					hit2 += 1
				break
		recsum2 += rec_rank

from matplotlib import pyplot as plt
keys = []
values = []
for i, j in sorted(Counter(rec_ranks).items(), key = lambda tup: tup[0]):
	keys.append(i)
	values.append(j)
plt.plot(keys, values, label = "freq")
keys = []
values = []
for i, j in sorted(Counter(rec_ranks2).items(), key = lambda tup: tup[0]):
	keys.append(i)
	values.append(j)
plt.plot(keys, values, label = "bigram")
plt.legend()
plt.savefig("eval.png")
print(recsum / count, hit / count)
print(recsum2 / count, hit2 / count)
