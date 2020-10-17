#!/usr/bin/env python
 
import socket
import array as arr

# Connect TCP/IP client to localhost in port 2500  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 2500))

# Open and read text file with cube state information
# NOTE: This is just an example to show the interaction with the cube simulator,
#		user must assemble the packets with the output of the vision algorithm
file = open("scramble.txt", "r")
str = file.read()
lines = str.split("\n")

# Assemble Set Cube State Command packet (see manual)
command = 0xFA
payloadLen = 48
packet = arr.array('B', [0] * (payloadLen + 2))
packet[0] = command
packet[1] = payloadLen
for idx in range(1, len(lines)):
	packet[idx + 1] = int(lines[idx][-1])

# Write packet to cube simulator
client.send(packet)
client.close()
