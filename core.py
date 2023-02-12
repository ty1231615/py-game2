import socket
import server
import element

print("loading...")
print(socket.gethostbyname(socket.gethostname()))
element.UserData.LOADS()
dataserver = server.SERVER()
dataserver.start()