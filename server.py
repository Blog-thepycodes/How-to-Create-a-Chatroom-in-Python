import socket
import threading
import datetime
 
 
HOST = '127.0.0.1'
PORT = 5050
 
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
 
 
clients = {}
chat_history = []
 
 
def handle_client(client, addr):
   print(f"[NEW CONNECTION] {addr} connected.")
 
 
   client.send("Enter your username: ".encode('utf-8'))
   username = client.recv(1024).decode('utf-8')
   clients[client] = username
 
 
   for message in chat_history:
       client.send(message.encode('utf-8'))
 
 
   broadcast(f"{username} joined the Pycodes chatroom.")
 
 
   while True:
       try:
           message = client.recv(1024).decode('utf-8')
           if message:
               if message.startswith('/users'):
                   list_users(client)
               else:
                   chat_history.append(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({username}): {message}")
                   broadcast(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({username}): {message}")
           else:
               remove_client(client)
               break
       except:
           remove_client(client)
           break
 
 
def broadcast(message):
   for client in list(clients.keys()):
       try:
           client.send(message.encode('utf-8'))
       except:
           remove_client(client)
 
 
def list_users(client):
   client.send(f"Online Users: {', '.join(clients.values())}".encode('utf-8'))
 
 
def remove_client(client):
   if client in clients:
       username = clients.pop(client)
       client.close()
       broadcast(f"{username} left the Pycodes chatroom.")
 
 
def start():
   server.listen()
   print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
 
 
   while True:
       client, addr = server.accept()
       clients[client] = ''
       threading.Thread(target=handle_client, args=(client, addr)).start()
 
 
print("[STARTING] Server is starting...")
start()
