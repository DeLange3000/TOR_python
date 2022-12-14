# libraries

# from crypt import *
import random
from socket import *
from random import *

serverPort = 12000
j = 2


clientName = '127.0.0.1'
clientSocket = socket(AF_INET, SOCK_DGRAM)

sentence = 'request relays 10'

clientSocket.sendto(str.encode(sentence), (clientName, serverPort))
msgFromServer, addr = clientSocket.recvfrom(1024)


print('From Server: ', msgFromServer.decode())
print(addr)
