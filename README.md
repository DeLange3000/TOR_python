# TOR_python

the project consists of 4 scripts (you should not run main.py) here is an overview on how to get everything running:

## GENERAL REMARKS:
If a message is recieved or send, the message and source/destination adress are printed
DO NOT RUN MAIN
If the relays script crashes of is stopped, then the server script should start again since the list of relays in the server is no longer correct.
Be carefull if you create too many relays in relays. Too big of a number will crash the program since there are too many relays for the select to handle. Limit the available relays to 500.
Be carefull if you select too many relays in Client. Limit the relays to around 50 in order to not crash the program.

## SERVER:
This is the TOR server and needs to be started first. You should not need to input anything.
It will run automatically. Once the message "The server is ready to recieve" is printed, then the TOR server is active
It will print out the list of relays if a relay is added
It will print out "sending relay info" if relay info is send to a Client
	
## RELAYS:
If the server is running, this script should be run. It asks "add relays?". 
If you type "y" or "Y" and press enter, then it asks "how many relays". Please input an integer bigger then 0 and press enter.
It will ask "how many relays" again if the input is not correct
If this is a succes, the relays are added to the TOR server. If the TOR server cannot be reached, no relay will work
After it received all answers from the TOR sever, it will ask again "add relays?".
If you type "y" or "Y" and press enter, more relays are added ON TOP OF the already existing relays
If you type "n" or "N" and press enter, all the relays that are added to the TOR server, become active. You need to do this before you start anything else.
It will show "elays are ready to recieve". IF THIS DOES NOT SHOW, DO NOT PROCEED. check if all previous steps are done correctly

## EXTERNAL SERVER:
if both server and relays are running, you can run the external_server script.
This needs no setup as the server and shows "The external server is ready to recieve"
Once this is shown, proceed to the next step
	
## CLIENT:
If server, relays and external_server are running, you can start the client script.
It shows "start TOR". If you type "y" or "Y" and press enter, then it will ask "message??".
Type in an message you want to send to the external server.
Then the client asks "how many relays?". Put in an integer number of the amount of relays you want to use.
Wait for response from external server

CONGRATS! you have succesfully run the TOR protocol locally on your computer.
