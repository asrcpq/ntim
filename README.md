# n-gram tiny input method(WIP)

(Chinese/Japanese support only)

## training

* Send cleaned corpus(contain characters to be learned only, line by line) to `ngram.py`

## Run

ntim is based on server-client mode(deamon is needed to load dictionary to RAM)

ntim server need a key-sequence-to-component mapper dictionary file,
it should be provided by `NTIM_MAPPER` environment variable.

## Todo

* [x] 1024 limit cut

* [ ] more than 2 chars

* [ ] probabilistic spelling solver

	* japanese key seq mapping

	* chinese heteronym

* [ ] IME occurrence probability
