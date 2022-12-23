# libraries

# from crypt import *
import random
import re
import textwrap
from socket import *
from random import *
from re import *
import rsa

from main import *



def getTORpackage(list_of_relays, message):

    package_to_send = message.encode()
    package_destination = ('127.0.0.1', 13000) #address of external server
    key = rsa.PublicKey.load_pkcs1(list_of_relays[0][1].encode(), format = "PEM")
    print(list_of_relays[0][0],"+",key)
    package_to_send = encrypt_long(b'l' +  str(package_destination).encode() + package_to_send, key)


    for i in range(1, len(list_of_relays)):
        next_addr = list_of_relays[i-1][0]
        #package_to_send = list_of_relays[i][0].encode() + ' '.encode() + package_to_send
        #print('package to send:',package_to_send)
        print('lenght of pkg', str(len(package_to_send)))
        #add encryption here
        key_pem = list_of_relays[i][1]
        #print("kpem:",key_pem.encode())
        key = rsa.PublicKey.load_pkcs1(key_pem.encode(), format = "PEM")
        #print(list_of_relays[i])
        #print("^:",key)
        #print("addr:",list_of_relays[i-1][0])
        enc_addr = encrypt_long(next_addr.encode(), key)
        #print("next:",next_addr)
        #print("enc:",enc_addr)
        #the enc addr is always 320 bytes long !!
        package_to_send = enc_addr + package_to_send
        
    #package_to_send = str(amount_of_relays) + package_to_send #so relay knows how many hops are left
    return [package_to_send, list_of_relays[-1][0]] #list_of_relays[-1] is first destination address


def check_msgFromServer(split_msgFromServer, relays_recieving, list_of_relays):
    #print("msg serv:",split_msgFromServer)
    key = ' '.join(split_msgFromServer[2:9])
    #print("key:",key)

    list_of_relays.append([split_msgFromServer[0] + ' ' + split_msgFromServer[1], key ])
    #print(list_of_relays)




#----------------MAIN FUNCTION----------------------------

serverPort = 12000
clientName = '127.0.0.1'
clientSocket = socket(AF_INET, SOCK_DGRAM)
print(clientSocket)
amount_of_relays = 0
relays_recieving = False

publicKey, privateKey = rsa.newkeys(128)

while True:
    inputt = input('start TOR? ')
    if( inputt == ( 'y' or 'Y')):

        #GET MESSAGE TO ENCRYPT
        message = input('message? ')
        # encMessage = encrypt_long(message.encode(), publicKey)
        # print("original string: ", message)
        # print("encrypted string: ", encMessage)
        # decMessage = decrypt_long(encMessage, privateKey).decode()

        # print("decrypted string: ", decMessage)
        #print('this is not a valid input')

        list_of_relays = []
        while True:
            try:
                amount_of_relays = int(input('how many relays? '))
                if(amount_of_relays > 1):
                    break
                else:
                    print('number needs to be bigger then 0')
            except:
                print('this is not a number')
                continue

        sentence = 'request relays ' + str(amount_of_relays)
        try:
            #ask server for relays
            clientSocket.sendto(str.encode(sentence), (clientName, serverPort))
            print('sending package: ', sentence, ' to: ', (clientName, serverPort))
            #server should send a relay in each response if TOR network is up
            counter = 0
            while counter < amount_of_relays + 1:
                try:
                    msgFromServer, addr = clientSocket.recvfrom(1024)
                    msgFromServer = msgFromServer.decode()
                    print(msgFromServer)
                    if(msgFromServer != ''):
                        if( msgFromServer == 'not enough relays available'):
                            print('not enough relays available')
                        split_msgFromServer = msgFromServer.split(' ')
                        #this is first message send from server before sending all the relays
                        if(split_msgFromServer[0] == 'list' and split_msgFromServer[1] == 'of' and split_msgFromServer[2] == 'relays:'):
                            relays_recieving = True
                            #print("counter:",counter)
                        if (relays_recieving):
                            if(counter != 0):
                                check_msgFromServer(split_msgFromServer, relays_recieving, list_of_relays)
                                #counter += 1
                            if(counter == amount_of_relays + 1):
                                relays_recieving = False
                                break
                            else:
                                counter += 1

                except:
                    print('destination could not be reached')
                    continue


        except:
            print('server cannot be reached')
            msgFromServer = ''
            continue

        print('creating TOR package')
        package_to_send, addr  = getTORpackage(list_of_relays, message) #encrypting package
        if (package_to_send != ''):
             addr = re.split('[()\', ]', addr)
             
             #send package to first relay
             clientSocket.sendto(package_to_send, (addr[2], int(addr[5])))
             print('sending TOR package: ', package_to_send, ' to: ', (addr[2], int(addr[5])))

        while True:
            try:
                #listen for reponse from server
                msgFromServer, addr = clientSocket.recvfrom(1024)
                msgFromServer = msgFromServer.decode()
                print('Server response: ', msgFromServer)
                break
            except:
                print('Server did not respond')
                continue

    if(inputt == ( 'n' or 'N')):
        quit()
        



