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

    print("incoming:", message)
    split_message =  re.split('[ ]', message)

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
                    #print(message)
                    #message[0] is public key , message[1] is private key
                    relay_list.append([addr, datetime.now(), message[0]]) #add relay to list
 #                   print('list: ', relay_list)
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
                #print("am:",amount_of_relays)
            except:
                response = 'NOT A NUMBER'
                return response

            if(len(relay_list) < amount_of_relays or len(relay_list) < 5):
                response = 'not enough relays available' #TOR needs enough relays to work
                return response
            else:
                response = ''
                range_of_a = []
                for i in range(0,len(relay_list)):
                    range_of_a.append(i)
                #print(range_of_a)
                try:
                    serverSocket.sendto(str('list of relays:').encode(), addr)
                except:
                    print('host not reachable')
                    return

                for i in range(0,amount_of_relays):

                    a = random.randint(0, len(range_of_a)-1) #create list of random relays, multiple relays are possible
                    #print("a:",a)
                    #print("range of a:", range_of_a) #debug
                    new_message = str(relay_list[i][0])+ ' ' + relay_list[i][2]
                    print(new_message)
                    range_of_a.remove(range_of_a[a]) #every relay is seperate
                    try:
                        serverSocket.sendto(str(new_message).encode(), addr)
                        print('sending relay info')
                    except:
                        print('host not reachable')
        else:
            response = 'YOUR MOM'
    return response

#checks if relays are still active
def check_relays():
    return

port = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))
print('The server is ready to receive')



#----------------MAIN FUNCTION------------------------------

while True:
    sentence, addr = serverSocket.recvfrom(2048)
    #decode message function here
    message = sentence.decode()
    response = check_message(message, addr)
    #encode message function here
    if response != '':
        serverSocket.sendto(str(response).encode(), addr)
        print('sending response: ', response, ' to: ', addr)






# def check_array():
#         for i in relay_list:
#             if(datetime.now() - relay_list(i,1) > 2000):
#                 serverSocket.sendto('still alive?', relay_list(i,1))
#                 print('still alive?')





