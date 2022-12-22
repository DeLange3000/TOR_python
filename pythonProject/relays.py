import datetime
import ipaddress
import multiprocessing
import subprocess
import selectors
import types
import sys
from socket import *
from random import *
from threading import *
from selectors import *
from time import sleep

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
relays = []
source_addr = [] #keeps the source addr of the packet send to relay so it can send it back once the response arrives
destination_addr = []
socket_addr = []

serverPort = 12000

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


def accept_wrapper(sock): #https://realpython.com/python-sockets/#handling-multiple-connections
    #print('size response array: ', len(source_addr))

    new_message = ''
    a = ''
    b = ''
    #print(sock)
    message, addr = sock.recvfrom(1024)  # Should be ready to read
    print(f"Accepted packet from {addr}")
    # data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # sel.register(conn, events, data=data)

    message = message.decode()
    print('incoming message: ',message)

    send_back_to_index = -1
    try:
        send_back_to_index = socket_addr.index(sock)
    except:
        print('message has not passed through here')
    if(send_back_to_index != -1):
        if(destination_addr[send_back_to_index] == addr):
            #add encryption here (this is for response from server)

            try:
                sock.sendto(str.encode(message), source_addr[send_back_to_index])
                print('sending message: ', message, ' to: ', source_addr[send_back_to_index])

            except:
                print('destination cannot be reached')

            source_addr.pop(send_back_to_index)
            destination_addr.pop(send_back_to_index)
            socket_addr.pop(send_back_to_index)
            return

    #add decryption here (from client to server)
    split_message = message.split(' ')
    #print(split_message)

    #add check to see if a "still alive" message has been send from the server?

    if len(split_message) > 3:
        try:
            a = split_message[0][2:len(split_message[0])-2] #socketname
            b = split_message[1][0:len(split_message[1]) - 1] #socketnumber
            #print(a)
            #print(b)
            #print(addr)
            source = (a, int(b))



            source_addr.append(addr) #source addr
            destination_addr.append(source) #dest addr
            socket_addr.append(sock) #current socket

            new_message = message[len(split_message[0]) + len(split_message[1]) + 2: len(message)]
            #print(new_message)
            sock.sendto(str.encode(new_message), (a, int(b)))
            print('sending new message: ', new_message, ' to: ', (a, int(b)))
            return
        except:
            sock.sendto(str.encode('bruh'), addr)
            print('sending response: ', 'bruh', ' to: ', addr)

    else:
        sock.sendto(str.encode('bruh bruh'), addr)
        print('sending response: ', 'bruh bruh', ' to: ', addr)


    return



    # data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # sel.register(conn, events, data=data)



def send_keys(relay, serverPort):
    relaySocket = socket(AF_INET, SOCK_DGRAM)
    relayName = '127.0.0.1'


    keyMessage = ''
    print(public_key_to_str(relay[1]))
    keyMessage += str(public_key_to_str(relay[1]))
    keyMessage += '@' #use @ to be recognised and split by the server
    keyMessage += str(public_key_to_str(relay[2]))
    keyMessage += '@'
    #print(keyMessage)
    return keyMessage

    # try:
    #     relaySocket.sendto(keyMessage, (relayName, serverPort))
    # except:
    #     print('server cannot be reached')

    #print(keyMessage) #debug

    #print(str.encode(keyMessage))

    return

def create_relays(serverPort):
    for i in range(0, amount_of_relays):
        current_time = datetime.now().time().microsecond
        relayName = '127.0.0.1'
        print(relayName)
        relaySocket = socket(AF_INET, SOCK_DGRAM)

        sentence = 'relay available'
        pubKey, privKey = rsa.newkeys(64)
        relay = send_keys([relaySocket, pubKey, privKey], serverPort)

        relaySocket.sendto(str.encode(sentence + ' ' + relay), (relayName, serverPort))
        print('sending message: ',sentence + ' ' + relay , ' to: ', (relayName, serverPort))
        waiting_for_response = True


        try:
            msgFromServer, addr = relaySocket.recvfrom(1024)

            #print('From Server: ', msgFromServer.decode(), addr)
            if(msgFromServer.decode() == 'added to relay list'):
                print('relay is added to server')

                relays.append([relaySocket, pubKey, privKey])

            else:
                print('relay could not be added to server')

        except:
            print('server broke connection')

    return relays



def decrypt_layer():
    return





#---------------------MAIN---------------------------

get_amount = True
serverPort = 12000
timeout = 10000
sel = selectors.DefaultSelector()

while True:
    a = input('add relays? ')
    if(a == ('n' or 'N')):
        if(len(relays) > 5):
            for i in range(0, len(relays)):
                relays[i][0].setblocking(False)
                sel.register(relays[i][0], selectors.EVENT_READ, data=None)
            print('relays are ready to recieve')
            process_running = False
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    # if key.data is None:
                    message = accept_wrapper(key.fileobj)


                #-------------------------------------------
        else:
            print('not enough relays')



    if(a == ('y' or 'Y')):
        try:
            amount_of_relays = int(input('how many relays? '))
            if(amount_of_relays > 0):
                get_amount = False
                relays = create_relays(serverPort)
            else:
                print('should be higher then 0')
        except:
            print('only numbers please')


        #send_keys(relays, serverPort) #addded this to create_relays function
        #print(relays)
