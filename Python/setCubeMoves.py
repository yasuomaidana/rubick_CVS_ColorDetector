#!/usr/bin/env python

import socket
import array as arr

# Dictionary of cube moves
movesDict = {
	"U":	0,
	"U2": 	1,
	"U'": 	2,
	"B": 	3,
	"B2": 	4,
	"B'": 	5,
	"R": 	6,
	"R2": 	7,
	"R'": 	8,
	"F": 	9,
	"F2": 	10,
	"F'": 	11,
	"L": 	12,
	"L2":	13,
	"L'":	14,
	"D": 	15,
	"D2":	16,
	"D'":	17
}

# Connect TCP/IP client to localhost in port 2500
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 2500))

# Open and read text file with cube moves information
# NOTE: This is just an example to show the interaction with the cube simulator,
#		user must assemble the packets with the output of the cube solution algorithm
file = open("movesSolution.txt", "r")
str = file.read()
lines = str.split("\n")
nMoves = len(lines) # number of moves detected in text file

# Assemble Set Cube Moves Command packet (see manual)
command = 0xFB
payloadLen = nMoves
packet = arr.array('B', [0] * (payloadLen + 2))
packet[0] = command
packet[1] = payloadLen
for idx in range(0, nMoves):
	cubeMove = lines[idx]
	packet[idx + 2] = movesDict[cubeMove]
	
# Write packet to cube simulator
client.send(packet)
client.close()
