# Read evaluated corpus from stdin
# each line, word to input should be split by space

import sys
import pickle
import ntim

ngrams = ntim.ngrams
input_mapper = ntim.input_mapper
recsum = 0
count = 0

for (idx, line) in enumerate(sys.stdin):
	if idx % 100 == 0:
		print(idx)
	segs = line.split()
	for seg in segs:
		try:
			spell = ngrams[len(seg)][seg][0][0] # use first candidates only
			candidates = input_mapper[spell]
			cand_counts = [ngrams[len(candidate)][candidate][1] for candidate in candidates]
			candidates_sorted = [x for x, _ in sorted(
				zip(candidates, cand_counts),
				key = lambda tup: tup[1],
				reverse = True,
			)]
			for (idx, candidate_in_count_order) in enumerate(candidates_sorted):
				if seg == candidate_in_count_order:
					rec_rank = 1 / (1 + idx)
		except KeyError:
			rec_rank = 0
		except IndexError:
			rec_rank = 0
		recsum += rec_rank
		count += 1

print(recsum / count, "with", count)
