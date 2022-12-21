# libraries

# from crypt import *
import random
import re
from socket import *
from random import *
from re import *
import rsa





def getTORpackage():

    package_to_send = 'get me www.openAI.com'

    for i in range(1, len(list_of_relays)):
        package_to_send = list_of_relays[i] + ' ' + package_to_send
        #add encryption here
    return [package_to_send, list_of_relays[0]] #list_of_relays[0] is first destination address


def check_msgFromServer(msgFromServer, relays_recieving, list_of_relays):
    if(relays_recieving == True):
        list_of_relays.append(msgFromServer)
    else:
        return



def encrypt_msg(): #using public keys of relays, in reverse order encrypt: message + addr of next hop
    return


#----------------MAIN FUNCTION----------------------------

serverPort = 12000
j = 2
clientName = '127.0.0.1'
clientSocket = socket(AF_INET, SOCK_DGRAM)
amount_of_relays = 0
relays_recieving = False

publicKey, privateKey = rsa.newkeys(512)

while True:
    if(input('start TOR? ') == ( 'y' or 'Y')):

        #GET MESSAGE TO ENCRYPT
        message = input('message? ')
        encMessage = rsa.encrypt(message.encode(), publicKey)
        print("original string: ", message)
        print("encrypted string: ", encMessage)
        decMessage = rsa.decrypt(encMessage, privateKey).decode()

        print("decrypted string: ", decMessage)
        #print('this is not a valid input')

        list_of_relays = []
        while True:
            try:
                amount_of_relays = int(input('how many relays? '))
                break
            except:
                print('this is not a number')

        sentence = 'request relays ' + str(amount_of_relays)
        try:
            clientSocket.sendto(str.encode(sentence), (clientName, serverPort))
            counter = 0
            while True:

                try:
                    msgFromServer, addr = clientSocket.recvfrom(1024)
                    msgFromServer = msgFromServer.decode()
                    print(msgFromServer)
                    if(msgFromServer != ''):
                        if( msgFromServer == 'not enough relays available'):
                            print('not enough relays available')
                        msgFromServer = msgFromServer.split(' ')
                        if(msgFromServer[0] == 'list' and msgFromServer[1] == 'of' and msgFromServer[2] == 'relays:'):
                            relays_recieving = True
                        check_msgFromServer(msgFromServer, relays_recieving, list_of_relays)


                    #print(counter)
                        if (relays_recieving):
                                if(counter == amount_of_relays + 1):
                                    relays_recieving = False
                                    break
                                else:
                                    counter += 1

                except:
                    print('destination could not be reached')

            package_to_send, addr  = getTORpackage()
        except:
            print('server cannot be reached')
            msgFromServer = ''



        if (package_to_send != ''):
             addr = re.split('[()\', ]', addr)
             #send package to first relay
             clientSocket.sendto(str.encode(package_to_send), (addr[2], int(addr[5])))

    if(input('start TOR? ') == ( 'n' or 'N')):
        break



