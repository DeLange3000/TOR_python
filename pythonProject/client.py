# libraries

# from crypt import *
import random
import re
from socket import *
from random import *
from re import *


def check_msgFromServer(msgFromServer):

    if( msgFromServer == 'not enough relays available'):
        print('not enough relays available')
        return ['', '']
    msgFromServer = msgFromServer.split(' ')
    if(msgFromServer[0] == 'list:'):
        for i in range(1, len(msgFromServer)-1, 2):
            list_of_relays.append(msgFromServer[i]+ ' ' + msgFromServer[i+1])
        #print(list_of_relays)

        package_to_send = 'get me www.openAI.com'

        for i in range(1, len(list_of_relays)):
            package_to_send = list_of_relays[i] + ' ' + package_to_send
            #add encryption here
        return [package_to_send, list_of_relays[0]] #list_of_relays[0] is first destination address



#----------------MAIN FUNCTION----------------------------

serverPort = 12000
j = 2
clientName = '127.0.0.1'
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    if(input('start TOR? ') == ( 'y' or 'Y')):
        list_of_relays = []
        while True:
            try:
                relays_amount = int(input('how many relays? '))
                break
            except:
                print('this is not a number')

        sentence = 'request relays ' + str(relays_amount)
        try:
            clientSocket.sendto(str.encode(sentence), (clientName, serverPort))
            msgFromServer, addr = clientSocket.recvfrom(1024)
            msgFromServer = msgFromServer.decode()
            print('From Server: ', msgFromServer)
            print(addr)
        except:
            print('server cannot be reached')
            msgFromServer = ''


        if(msgFromServer != ''):
            package_to_send, addr = check_msgFromServer(msgFromServer)
            #print(addr)
            #print('total package: ',package_to_send)
            #print(list_of_relays)
            if (package_to_send != ''):
                addr = re.split('[()\', ]', addr)
                #send package to first relay
                clientSocket.sendto(str.encode(package_to_send), (addr[2], int(addr[5])))

                try:
                    msgFromServer, addr = clientSocket.recvfrom(1024)
                except:
                    print('destination could not be reached')

    if(input('start TOR? ') == ( 'n' or 'N')):
        break
    else:
        print('this is not a valid input')


