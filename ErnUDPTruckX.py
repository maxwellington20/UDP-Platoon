# Program to simulate leading truck
# by Maxwell Ern, 
# The following program builds on the the following project by 
# communicating with multiple servers. Largely unchanged. 

import socket
import time

#initial client values, mostly taken from provided project files
seq_num = 5895
port_to_Y = 5679
port_to_Z = 5678
pos = "14 S 368052 3899189"
vel = 110.0
t_sec = 0.2
accel = 1.38
brk_ctrl = 0.0
throttle = 0.46

#just for clarity's sake when viewing the three terminals
print("============================================")
print("==============> TruckX Log <================")
print("============================================\n")


#####################
# Definitions Below #
#####################

#prepare client_pack data
def createPacket():
    client_pack = "X," + str(seq_num) + "," + str(addr) + "," + str(pos) + "," + str(vel)
    client_pack += "," + str(accel) + "," + str(brk_ctrl) + "," + str(throttle) + ","
    return str.encode(client_pack) #convert list of variables to bytes

#print packet info
def printPacketSent(port_num):
    truck = ""
    if (port_num == port_to_Y):
        truck = "Truck Y"
    elif (port_num == port_to_Z):
        truck = "Truck Z"
    else: 
        truck = "Unknown Port Number"
    print("Packet Sent to %s:" %(truck))

    if(seq_num == 99999): # signals that client will disconnect from server
        print("Type = Socket Disconnection")
        print("Sequence No. = 99999\n")
        clientSock.close()
        quit()

    print("Sequence No. = %d" %(seq_num))
    print("IP = %s" %(addr))
    print("GPS Position = %s" %(pos))
    print("Velocity = %.2f" %(vel))
    print("Acceleration = %.2f" %(accel))
    print("Brake Control = %.1f" %(brk_ctrl))
    print("Gas Throttle = %.2f\n" %(throttle))

#print ack info
def printPacketRecv(num, port_num):
    truck = ""
    if (port_num == port_to_Y):
        truck = "Truck Y"
    elif (port_num == port_to_Z):
        truck = "Truck Z"
    else: 
        truck = "Unknown Port Number"
    print("Packet Received from %s:" %(truck))
    print("Type = Ack")
    print("Sequence No. = %s\n" %(num))
    

##################
# The Rest Of It #
##################

#connect to server
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#get ip address
addr=socket.gethostbyname(socket.gethostname())
if addr=="127.0.0.1":
    print("No internet, your localhost is "+ addr)
else:
    print("Connected with IP address: "+ addr)

#print initial values
print("\nInitial GPS Position: %s" %(pos))
print("Initial Velocity: %.1fkm/h" %(vel))
print("Time Interval: %.1fs" %(t_sec))
print("============================================")

def sendAndReceive(serv_addr, port_num): #made this to streamline the testing proccess
    #send client packet
    data = createPacket()
    clientSock.sendto(data, (serv_addr, port_num))
    printPacketSent(port_num)

    while True:
        time.sleep(t_sec) #wait a bit before looking to recieve
        data, serv_addr = clientSock.recvfrom(1024) #recieve server packet
        serv_pack = bytes.decode(data)
        printPacketRecv(serv_pack, port_num)
        break

sendAndReceive(addr, port_to_Y) #execute with original info
sendAndReceive(addr, port_to_Z)

while True:
    n = input("Finished? (y/n): ")
    if (n == "y"):
        quit()



