# n-gram tiny input method(WIP)

## training

* Send cleaned corpus(contain characters to be learned only, line by line) to `ngram.py`

* `NTIM_EXACT_MAPPER` and `NTIM_CHAR_MAPPER` are 2 env files
read by `ngram.py`
that map key sequence to input word char by char
(all possible combinations are used)
or by whole string.

example(exact mapper):

```
zirjma 自然码
nyuryoku 入力
```

## Run

ntim is based on server-client mode(deamon is needed to load dictionary to RAM)

## Todo

* [x] 1024 limit cut

* [x] more than 2 chars

* [x] reduce dict size(2+)

* [x] dict size limiter(probability problem)

* [x] partial input buffer match

	* [ ] delete still match longer

* [ ] evaluator

* [ ] fix probability

* [ ] IME occurrence probability(revise count)

* [ ] probabilistic spelling solver(heteronym)

* [ ] merge ntim data
