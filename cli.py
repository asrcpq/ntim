import sys
import curses
import atexit
import signal
import socket
import pickle

def handle_exit(*args):
	curses.nocbreak()
	curses.echo()
	stdscr.keypad(False)
	curses.endwin()
	sys.exit()

atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
buffer = ""
input_buffer = ""
candidates = []
page_offset = 0
wpp = 5
file = open("/tmp/ntim", "w")

def handle_input(ch) -> bool:
	global input_buffer
	global buffer
	global candidates

	if chint == -1 or chint == 3:
		sys.exit()
	if chint == 263 or chint == 8: # curses is shit
		if len(input_buffer) > 0:
			input_buffer = input_buffer[:-1]
			return True
		elif len(buffer) > 0:
			buffer = buffer[:-1]
			return False
	if chint == 10 and input_buffer == "":
		file.write(buffer)
		sys.exit()

	flag = True
	if chint == 6:
		if page_offset + wpp < len(candidates):
			page_offset += wpp
	elif chint == 2:
		if page_offset >= wpp:
			page_offset -= wpp
	else:
		flag = False
	if flag:
		return False
	else:
		page_offset = 0

	flag = True
	if chint == ord('0'):
		idx = page_offset + wpp - 1
	elif ord('1') <= chint <= ord('9'):
		idx = page_offset + int(chr(chint)) - 1
	elif chint == ord(' '):
		idx = page_offset
	elif chint == 10:
		buffer += input_buffer
		input_buffer = ""
		return False
	else:
		flag = False
	if flag:
		if idx < len(candidates):
			buffer += candidates[idx]
			input_buffer = ""
			candidates = []
		return False

	if ord('a') <= chint <= ord('z'):
		input_buffer += chr(chint)
		return True

	return False

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as socket:
	socket.connect("ntim.socket")
	while True:
		chint = stdscr.getch()
		print(chint, file = sys.stderr)
		recompute_flag = handle_input(chint)

		if recompute_flag:
			if input_buffer:
				encoded = bytes(f"{input_buffer} s{buffer}", "utf-8")
				socket.sendall(encoded)
				candidates = pickle.loads(socket.recv(1024))
			else:
				candidates = []
	
		stdscr.clear()
		stdscr.addstr(0, 0, buffer) # 0 is start marker
		stdscr.addstr(1, 0, input_buffer)
		stdscr.addstr(2, 0, " ".join(candidates[page_offset: page_offset + wpp]))
