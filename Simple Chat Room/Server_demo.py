import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

# Lists for clients and their nicknames
clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)


def handle(client):
	while True:
		try:
			# Broadcasting message
			message = client.recv(1024)
			broadcast(message)
		except:
			# Removing and closing the clients
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast('{} left!'.format(nickname).encode('ascii'))
			nicknames.remove(nickname)
			break

#Receving /Listening function
def receive():
	while True:
		# Accept Connection
		client,address = server.accept()
		print("Connected with {}".format(str(address)))

		# Request and Store Nickname
		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)

		# Print and Broadcast Nickname
		print("Nickname is{}".format(nickname))
		broadcast("{} joined!".format(nickname).encode('ascii'))
		client.send('Connected to Server!'.encode('ascii'))

		# Start Handling the thread for client
		thread =threading.Thread(target = handle,args=(client,))
		thread.start()

print("Server is listening...")
receive()
