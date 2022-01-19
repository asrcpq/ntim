# n-gram tiny input method(WIP)

(support zh-ziranma and ja-romaji natively,
or you need to implement your own key sequence interpreter)

## training

* Send cleaned corpus(contain characters to be learned only, line by line) to `ngram.py`

## Run

ntim is based on server-client mode(deamon is needed to load dictionary to RAM)

## Todo

* [x] 1024 limit cut

* [ ] more than 2 chars

* [ ] probabilistic spelling solver

	* japanese key seq mapping

	* chinese heteronym

* [ ] IME occurrence probability
