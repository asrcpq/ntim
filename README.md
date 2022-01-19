# n-gram tui input method(WIP)

## training

* Send cleaned corpus(contain characters to be learned only, line by line) to `ngram.py`

## Run

ntim is based on server-client mode(deamon is needed to load dictionary to RAM)

ntim server need a key-sequence-to-component mapper dictionary file,
it should be provided by `NTIM_MAPPER` environment variable.

## Todo

* 1024 limit cut

* more than 2 chars

* japanese key seq mapping

* chinese duoyinzi probability

* revise word probability
