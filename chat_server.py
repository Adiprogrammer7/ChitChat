import socket
from threading import Thread 
from addr_info import IP, PORT

if not IP:
	print("Please make sure that you entered ip and port in addr_info.py file!")

BUFFSIZE = 1024
CONN_USERNAME = {} #conn socket will be key and username of client would be value.

class Server:
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((IP, PORT))
		self.server_socket.listen(7)
		print("Waiting for connections...")
		self.a_thread = Thread(target= self.accept_client)
		self.a_thread.start()
		self.a_thread.join()
		self.server_socket.close()

	def accept_client(self):
		# Accepting new client connection
		while True:
			self.conn, self.addr = self.server_socket.accept()  #self.conn is new socket obj created for communication bet. server and client, self.addr is clients addr.
			print(f'{self.addr} has connected.')
			self.username = self.conn.recv(BUFFSIZE).decode("utf-8")
			self.conn.send(str.encode("Welcome to ChitChat app!"))  #sending to client.
			self.msg_of_joined = f'{self.username} has joined the chatroom!'
			print(self.msg_of_joined)
			self.broadcast(self.msg_of_joined)  #to send this msg to all clients.
			CONN_USERNAME[self.conn] = self.username  #adding conn socket and username to a dict.

			# Thread for handling client.
			self.h_thread = Thread(target=self.handle_client, args= (self.conn,))
			self.h_thread.start()

	def handle_client(self, conn):
		# receiving and broadcasting messages.
		while True:
			try:
				self.msg = conn.recv(BUFFSIZE).decode('utf-8') 	
				self.broadcast(f'{self.msg}')
			except Exception:
				username = CONN_USERNAME[conn] #temp. storing name as we are deleting it next.
				del CONN_USERNAME[conn] 
				self.broadcast(f'{username} has left the chatroom!')
				print(f'{username} has left the chatroom!')
				break

	def broadcast(self, msg):
		# distributing msg of one client with all clients.
		for conn_socket in CONN_USERNAME:
			conn_socket.send(str.encode(msg))

s = Server()
