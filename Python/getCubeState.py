#!/usr/bin/env python
 
import socket
import array as arr

# Connect TCP/IP client to localhost in port 2500  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 2500))

# Assemble Set Cube State Command packet (see manual)
command = 0xFC
packet = arr.array('B', [0] * 1)
packet[0] = command;

# Write packet to cube simulator
client.send(packet)

# Read Cube State from cube simulator (48 bytes)
cubeState = client.recv(48);

print(cubeState);

client.close()
