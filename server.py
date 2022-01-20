import os
import socket
import var
import ntim
import pickle

socket = socket.socket(socket.AF_UNIX,  socket.SOCK_STREAM)
socket_path = "ntim.socket"
socket.bind(socket_path)
socket.listen(1)
try:
	while True:
		connection, address = socket.accept()
		print("connected from", address)
		while True:
			data = connection.recv(var.msg_len)
			#print("recv: ", data)
			if not data:
				break
			decoded = data.decode('utf-8').strip()
			input_buffer, buffer = decoded.split(" ", 1)
			candidates = ntim.get_candidates(input_buffer, buffer)
			#print("send: ", candidates)
			connection.send(pickle.dumps(candidates))
finally:
	socket.close()
	os.remove(socket_path)
