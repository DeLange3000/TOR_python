import datetime
import ipaddress
import multiprocessing
import subprocess
import selectors
import types
import sys
import re
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

from main import *

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
    
    #pk = PublicKey.save_pkcs1(public_key, format='PEM')
    #print(pk)
    #print(pk.decode("ascii"))
    #split = pk.decode().split('\n')
    #pk = split[1]
    return PublicKey.save_pkcs1(public_key, format='PEM').decode("ascii")

def accept_wrapper(sock): #https://realpython.com/python-sockets/#handling-multiple-connections
    #print('size response array: ', len(source_addr))

    new_message = ''
    a = ''
    b = ''
    #print(sock)
    message, addr = sock.recvfrom(16384)  # Should be ready to read
    print("this is:",sock,f"Accepted packet from {addr}")
    # data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # sel.register(conn, events, data=data)

    
    #print('incoming message: ',message)
    print('incoming message length: ',len(message))
        

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
    
    try:
        #add decryption here (from client to server)
        #get correct private key for current socket
        #print(sock)
        _, _, currPrivKey = [relay for relay in relays if relay[0] == sock][0]
        print("priv:",currPrivKey)
    
        next_addr = decrypt_long(message[0:320], currPrivKey)
        print("decrypted addr:", next_addr)
        rest_msg = message[320:]
        if next_addr[0] == b'l'[0]: # signifies last relay before end -> decrypt everything, also     rest_msg
            next_addr = next_addr[1:]
            rest_msg = decrypt_long(rest_msg, currPrivKey).lstrip(b'l')
        #print("rest_:",rest_msg)
        split_message = message.split(b' ')
        #print("split msg:",split_message)
    
        #add check to see if a "still alive" message has been send from the server?
    
     #   if len(split_message) > 3:
     #       try:
     #           a = split_message[0][2:len(split_message[0])-2] #socketname
     #           b = split_message[1][0:len(split_message[1]) - 1] #socketnumber
     #           #print(a)
     #           #print(b)
     #           #print(addr)
     #           source = (a, int(b))
    #
    #
    #
     #           source_addr.append(addr) #source addr
     #           destination_addr.append(source) #dest addr
     #           socket_addr.append(sock) #current socket
    #
     #           new_message = message[len(split_message[0]) + len(split_message[1]) + 2:     len(message)]
     #           #print(new_message)
     #           sock.sendto(str.encode(new_message), (a, int(b)))
     #           print('sending new message: ', new_message, ' to: ', (a, int(b)))
     #           return
     #       except:
     #           sock.sendto(str.encode('bruh'), addr)
     #           print('sending response: ', 'bruh', ' to: ', addr)
    #
     #   else:
    
        next_addr_arr = [next_addr[2:11].decode(), next_addr[14:19].decode()]
    
        #send package to next relay
        sock.sendto(rest_msg, (next_addr_arr[0], int(next_addr_arr[1])))
        #print('sending TOR package: ', rest_msg, ' to: ', (next_addr_arr[0], int(next_addr_arr[1])))
    
            #sock.sendto(str.encode('bruh bruh'), addr)
            #print('sending response: ', 'bruh bruh', ' to: ', addr)

    except:
        print("could not understand message")
    return



    # data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    # events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # sel.register(conn, events, data=data)



def send_keys(relay, serverPort):
    relaySocket = socket(AF_INET, SOCK_DGRAM)
    relayName = '127.0.0.1'


    keyMessage = ''
    #print(public_key_to_str(relay[1]))
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
        pubKey, privKey = rsa.newkeys(128)
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



def decrypt_layer(message, addr):

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
            print('relays are ready to receive')
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
                print('should be higher than 0')
        except:
            print('only numbers please')


        #send_keys(relays, serverPort) #addded this to create_relays function
        #print(relays)
