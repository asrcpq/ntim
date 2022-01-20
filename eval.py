# Read evaluated corpus from stdin
# each line, word to input should be split by space

import sys
import pickle
import ntim

ngrams = ntim.ngrams
input_mapper = ntim.input_mapper
recsum = 0
count = 0
recsum2 = 0
count2 = 0

for (idx, line) in enumerate(sys.stdin):
	if idx % 100 == 0:
		print(idx)
	segs = line.split()
	for (i, seg) in enumerate(segs):
		# simple freq
		try:
			rec_rank = 0
			spell = ngrams[len(seg)][seg][0][0] # use first candidates only
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
		recsum += rec_rank
		count += 1

		# ngram prediction
		rec_rank = 0
		if i == 0:
			buf = 's'
		else:
			buf = segs[i - 1][-1]
		candidates_sorted = ntim.get_candidates(seg, buf)
		print(candidates_sorted)
		for (idx, candidate_in_count_order) in enumerate(candidates_sorted):
			if seg == candidate_in_count_order:
				rec_rank = 1 / (1 + idx)
		recsum2 += rec_rank
		count2 += 1

print(recsum / count, "with", count)
print(recsum2 / count2, "with", count2)

