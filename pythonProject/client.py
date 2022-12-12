# libraries

# from crypt import *
import random
from socket import *
from random import *

clientSockets = []
get_amount = True
serverPort = 12000
j = 2

while True:
    while get_amount:
        try:
            print('how many relays?')
            amount_of_relays = int(input())
            get_amount = False
        except:
            print('only numbers please')

    for i in range(0,amount_of_relays):

        clientName = '127.0.0.'+str(j)
        j = j + 1
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        sentence = 'request'

        clientSocket.sendto(str.encode(sentence), (clientName, serverPort))
        msgFromServer, addr = clientSocket.recvfrom(1024)
        clientSockets.append(clientSocket, True)

        print('From Server: ', msgFromServer.decode(), addr)

    get_amount = True