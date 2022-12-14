import datetime
from socket import *
from random import *

# libraries

# from crypt import *
import random
from socket import *
from datetime import *
from random import *

get_amount = True
serverPort = 12000
timeout = 10000

j = 2

while True:
    while get_amount:
        try:
            print('how many relays?')
            amount_of_relays = int(input())
            get_amount = False
        except:
            print('only numbers please')

    for i in range(0, amount_of_relays):
        current_time = datetime.now().time().microsecond

        relayName = '127.0.0.'+str(j)
        j = j + 1
        relaySocket = socket(AF_INET, SOCK_DGRAM)

        sentence = 'relay available'

        relaySocket.sendto(str.encode(sentence), (relayName, serverPort))
        waiting_for_response = True


        try:
          msgFromServer, addr = relaySocket.recvfrom(1024)
          print('From Server: ', msgFromServer.decode(), addr)
        except:
            print('server broke connection')


    get_amount = True