# libraries

# from crypt import *
import time
from socket import *
from datetime import *
relay_list = [] #saves address, time at last response

port = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))
print('The server is ready to recieve')
while True:
    sentence, addr = serverSocket.recvfrom(1024)

    if(sentence.decode() == 'request'):
        relay_list.append([addr, datetime.now()])
        print('list: ', relay_list)
    capitalizedSentence = sentence.upper()
    serverSocket.sendto(str(capitalizedSentence).encode(), addr)



def check_array():
        for i in relay_list:
            if(datetime.now() - relay_list(i,1) > 2000):
                serverSocket.sendto('still alive?', relay_list(i,1))
                print('still alive?')







