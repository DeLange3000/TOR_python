# libraries
import rsa

def encrypt_long(bytes, pubkey):
    outp = b''
    for byte in bytes:
        enc = rsa.encrypt(byte.to_bytes(1, 'big'), pubkey)
        outp += enc
    return outp
    
def decrypt_long(bytes, privkey):
    outp = b''
    bytes_group = [bytes[i:i + 16] for i in range(0, len(bytes), 16)]
    print("bgroup:",bytes_group)
    for bytes_16 in bytes_group:
        #print(bytes_16)
        dec = rsa.decrypt(bytes_16, privkey)
        #print("dec:",dec)
        outp += dec
    return outp

# peer reaches server to say it wants to join tor network
# peer recieves message from server if it is joined
# peer choses amount of relays (same relays can be used more then once)
# peer reaches out to server to get a list of random available relays (server sends list of relay addresses)
# peer encodes the same amount of times as relays are requested and sends the packet to first relay
# the first relay decodes first encoding and sends to next relay but source address is first relay
# continue until amount of relays is enough

# response is send to last relay
# last relay encrypts and sends to previous relay (relays should keep source address of last recieved package)
# continue until peer is reached (encrypt at each relay)

# encryption:
# for package going from peer to server and hopping over relays
# peer encrypts layers for each relay with their public key
# then each relay can decrypt next layer with their private key

# for package going from server to peer
# package is encrypted at last relay with its private key
# send to next relay and encrypt with private key
# continue until peer is reached
# peer knows correct order in which to apply the public keys to decrypt the packet

# server:
# server needs to update list of relays periodically (encrypted, maybe key?)
# timeout to check if peer is still available (if timeout is reached send udp to peer to check availability)
# accept and send messages to peers that want to use TOR (agree on key?)


# peers:
# needs to connect to TOR server (encryption should be used)
# should be able to recieve list of relays (encrypted) of TOR server
# needs to have access to public keys of relays
#encryption form: (destination) (encrypted package) -> reciever already knows source and should keep it until answer from server returns

# relays
# needs to keep address to which relay it will send package if it returns from server -> use ports on relays so when server returns package to specific port, the relay knows to which other relay it needs to send the package to
# needs a private key
# needs to communicate with TOR to let it know if it is up or down

#implement everything without encryption, if everything works, add encryption
