import datetime
import ipaddress
import multiprocessing
import subprocess
from socket import *
from random import *

# libraries
import rsa
from rsa import *

# from crypt import *
import random
from ipaddress import *
from socket import *
from datetime import *
from random import *
from multiprocessing import *
from subprocess import *

continue_ = True

def public_key_to_str(public_key): #from https://python.hotexamples.com/examples/rsa/PublicKey/save_pkcs1/python-publickey-save_pkcs1-method-examples.html
    """ This function produces a string that represents the public key in PEM
        format. This way it can be written to a database or transferred accross
        an internet connection.

    Args:
        public_key (rsa.PublicKey): The key that is to be interpreted to a
                                    PEM-format string.
    Returns:
        bytearray: A string of bytes representing the key in PEM format.
    """
    return PublicKey.save_pkcs1(public_key, format='PEM')

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

                pubKey, privKey = rsa.newkeys(64)

                relays.append([relaySocket, pubKey, privKey])
            else:
                print('relay could not be added to server')

        except:
            print('server broke connection')

    return relays

def send_keys(relays, serverPort):
    relaySocket = socket(AF_INET, SOCK_DGRAM)
    relayName = '127.0.0.1'
    keyMessage = b''

    for relay in relays:
        print(public_key_to_str(relay[1]))
        keyMessage += public_key_to_str(relay[1])
        keyMessage += b'@' #use @ to be recognised and split by the server
        keyMessage += public_key_to_str(relay[2])
        keyMessage += b'@'

    relaySocket.sendto(keyMessage, (relayName, serverPort))
    print(keyMessage) #debug
    #print(str.encode(keyMessage))
    return

def decrypt_layer():
    return





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
                    process = multiprocessing.Process(target = Running_relays ,args = (str(relays[i][0]))) #run all relays at same time
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
        send_keys(relays, serverPort)
        #print(relays)