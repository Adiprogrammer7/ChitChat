import socket
from threading import Thread 
import tkinter as tk
from addr_info import IP, PORT

if not IP:
	print("Please make sure that you entered ip and port in addr_info.py file!")


BUFFSIZE = 1024

class Client:
	def __init__(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((IP, PORT))
		print("Connected to server!")
		self.username_widget()
		self.chatroom_widget()

	def username_widget(self):
		self.root = tk.Tk()
		self.root.title("ChitChat")
		self.root.geometry("400x200")
		self.username_label = tk.Label(self.root, text= "Enter username: ", font=('Comic Sans MS', 24), anchor= 'center', pady= 10)
		self.username_label.pack()
		self.username_entry = tk.Entry(self.root, justify= 'center', bd= 3, font=('Comic Sans MS', 16), fg= 'blue')
		self.username_entry.pack()
		self.submit_btn = tk.Button(self.root, text= "Submit", font=('Comic Sans MS', 12, 'underline'), fg= 'green', justify= 'center', command= self.submit_username)
		self.submit_btn.pack()
		self.root.bind('<Return>', self.submit_username)  
		tk.mainloop()

	# Sending username to server.
	def submit_username(self, event= None):
		self.username = self.username_entry.get()
		if self.username:
			self.client_socket.send(str.encode(self.username)) 
			self.root.destroy()

	def chatroom_widget(self):
		root = tk.Tk()
		root.title("ChitChat")
		messages_frame = tk.Frame(root)
		self.my_msg = tk.StringVar()  # variable for the messages to be sent.
		self.my_msg.set("type here...")
		scrollbar = tk.Scrollbar(messages_frame)  
		self.msg_list = tk.Listbox(messages_frame, height=15, width=55, yscrollcommand=scrollbar.set, font= ('Consolas', 14))
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
		self.msg_list.pack()
		messages_frame.pack()
		entry_field = tk.Entry(root, textvariable=self.my_msg, font= ('Consolas', 16), fg= 'green', width= 40, bd= 4)
		entry_field.bind("<Return>", self.send)
		entry_field.pack()
		send_button = tk.Button(root, text="Enter", font=('Comic Sans MS', 12), command= self.send, bd= 4)
		send_button.pack()
		# Thread for receive function
		self.receive_thread = Thread(target= self.receive)
		self.receive_thread.start()	
		tk.mainloop()

	def receive(self):
		while True:
			try:
				self.msg = self.client_socket.recv(BUFFSIZE).decode("utf-8")
				if self.msg:
					self.msg_list.insert(tk.END, self.msg) #adding received msg to chatroom widget.
					# to always remained scrolled to last msg.
					self.msg_list.select_clear(self.msg_list.size() - 2)
					self.msg_list.select_set(tk.END)
					self.msg_list.yview(tk.END)

			except Exception as e:
				print(str(e))
				break

	def send(self, event= None):
		msg = self.my_msg.get()
		self.my_msg.set("")  # Clears input field.
		if msg:
			self.client_socket.send(str.encode(self.username + ': ' + msg))

c = Client()
