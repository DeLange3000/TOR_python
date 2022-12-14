import datetime
import ipaddress
import multiprocessing
import subprocess
from socket import *
from random import *

# libraries

# from crypt import *
import random
from ipaddress import *
from socket import *
from datetime import *
from random import *
from multiprocessing import *
from subprocess import *

continue_ = True

def Running_relays(relay):
    print('parallel process started')
    #sentence, addr = relay.recvfrom(1024)
    #print('packet recieved')

    #process incoming packet

def create_relays(serverPort):
    for i in range(0, amount_of_relays):
        current_time = datetime.now().time().microsecond
        relayName = '127.0.0.1'
        print(relayName)
        relaySocket = socket(AF_INET, SOCK_DGRAM)

        sentence = 'relay available'

        relaySocket.sendto(str.encode(sentence), (relayName, serverPort))
        waiting_for_response = True


        try:
            msgFromServer, addr = relaySocket.recvfrom(1024)
            print('From Server: ', msgFromServer.decode(), addr)
            if(msgFromServer.decode() == 'added to relay list'):
                print('relay is added to server')
                relays.append(relaySocket)
            else:
                print('relay could not be added to server')

        except:
            print('server broke connection')

    return relays







#---------------------MAIN---------------------------

get_amount = True
serverPort = 12000
timeout = 10000
relays = []

while True:
    a = input('add relays? ')
    if(a == ('n' or 'N')):
        if(len(relays) > 5):
            while True:
                print('relay can recieve packages')
                processes = []
                for i in range(0,len(relays)):
                    #------NEEDS TO BE FIXED---------------
                    process = multiprocessing.Process(target = Running_relays ,args = (str(relays[i]))) #run all relays at same time
                    processes.append(process)
                    process.start()

                b = 0
                while continue_:
                    b = b + 1

                for i in processes:
                    i.join()

                #-------------------------------------------
        else:
            print('not enough relays')



    if(a == ('y' or 'Y')):
        try:
            amount_of_relays = int(input('how many relays? '))
            get_amount = False
        except:
            print('only numbers please')

        relays = create_relays(serverPort)
        print(relays)
