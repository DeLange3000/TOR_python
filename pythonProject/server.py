# libraries

# from crypt import *
import random
import time
import re
from socket import *
from datetime import *
from re import *
relay_list = [] #saves address, time at last response
relay_indexes = []

#checks incoming mesages and handles them
def check_message(message, addr):

    split_message =  re.split('[ ]', message)
    print(split_message)

    if len(split_message) < 2: #check if message is not too big or too small
        response = 'YOUR MOM'
    else:
        if( split_message[0]== 'relay' and split_message[1] == 'available'): #if relay wants to join TOR
            try:
                relay_list.index(addr) #check if relay isnt already in the list
                response = 'you are already on the list'
            except:
                try:
                    message = re.split('[@]', message[len(split_message[0])+len(split_message[1]) + 2 : len(message)])
                    #message[0] is public key , message[1] is private key
                    relay_list.append([addr, datetime.now(), message[0], message[1]]) #add relay to list
                    print('list: ', relay_list)
                    response = 'added to relay list'
                except:
                    response= 'no key send'

        elif( split_message[0]== 'relay' and split_message[1] == 'not' and split_message[2] == 'available'): #when relay is no longer available
            try:
                index = relay_list.index(addr)
                relay_list.remove(index)
                response = 'you are removed from list'
            except:
                response = 'you are not even on the list' #check relay was on the list

        elif(split_message[0] == 'request' and split_message[1] == 'relays'): #peer can request list of relays

            try:
                amount_of_relays = int(split_message[2]) #check if an actual number is requested
            except:
                response = 'NOT A NUMBER'

            if(len(relay_list) < 5):
                response = 'not enough relays available' #TOR needs enough relays to work
            else:
                response = 'list:'
                prev_a = -1
                #moeten we nie volledige lijst relays sturen, en de client zelf een random selectie laten doen ? zodat het pad ongekend is voor de server
                relay_indexes = []
                for i in range(0, amount_of_relays):
                    a = random.randint(0, len(relay_list) - 1) #create list of random relays, multiple relays are possible
                    print(a) #debug
                    while a == prev_a: #make sure sequential relays are not the same relays
                        a = random.randint(0, len(relay_list)) #choose new random value until they are not the
                    response = response +' ' + str(relay_list[a][0])
                    # for relay in relay_indexes:
                    #     serverSocket.sendto(str(relays[a]).encode(), addr)
                    relay_indexes.append(a)
                    prev_a = a
        else:
            response = 'YOUR MOM'
    return response

#checks if relays are still active
def check_relays():
    return

port = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))
print('The server is ready to recieve')



#----------------MAIN FUNCTION------------------------------

while True:
    sentence, addr = serverSocket.recvfrom(2048)
    #decode message function here
    message = sentence.decode()
    response = check_message(message, addr)
    #encode message function here
    serverSocket.sendto(str(response).encode(), addr)






# def check_array():
#         for i in relay_list:
#             if(datetime.now() - relay_list(i,1) > 2000):
#                 serverSocket.sendto('still alive?', relay_list(i,1))
#                 print('still alive?')





