# libraries

# from crypt import *
import random
import time
import re
from socket import *
from datetime import *
from re import *


port = 13000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))
print('The external server is ready to recieve')



#----------------MAIN FUNCTION------------------------------

while True:
    sentence, addr = serverSocket.recvfrom(2048)
    #decode message function here
    message = sentence.decode()
    print('from client: ', message)

    response = 'response from external server for: ' + message
    #encode message function here
    if response != '':
        try:
            serverSocket.sendto(str(response).encode(), addr)
            print(print('sending response: ', response, ' to: ', addr))
        except:
            print('destination not available')






# def check_array():
#         for i in relay_list:
#             if(datetime.now() - relay_list(i,1) > 2000):
#                 serverSocket.sendto('still alive?', relay_list(i,1))
#                 print('still alive?')





