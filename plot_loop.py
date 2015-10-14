#!/usr/bin/python
#!/usr/bin/env python
 
import csv
import matplotlib.pyplot as plt
import sys

 
# for P lines
#0-> str,
#1 -> clock_time(),2-> P, 3->rimeaddr_node_addr.u8[0],rimeaddr_node_addr.u8[1], 4-> seqno,
#5 -> all_cpu,6-> all_lpm,7-> all_transmit,8-> all_listen,9-> all_idle_transmit,10-> all_idle_listen,
#11->cpu,12-> lpm,13-> transmit,14-> listen, 15 ->idle_transmit, 16 -> idle_listen, [RADIO STATISTICS...]
 
 
from collections import defaultdict
cpuOverTime =  defaultdict(list)


numOfMsgs = 20
nodeID = 12
msgLeft = True
msgID = 0
rece = [0] * (numOfMsgs + 1)
send = [0] * (numOfMsgs + 1)
radioOn = 0
radioCount = 0
totalSend = 0
totalRecv = 0
count = 0

if len(sys.argv) == 3:
	numOfMsgs = int(sys.argv[1])
	nodeID = int(sys.argv[2])
	print "Number of message", numOfMsgs, " Node ID:", nodeID 


with open('test1.csv', 'rU') as f:
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		#Package delivery rate
		msgID = 0
		while msgID < numOfMsgs:
			msgID = msgID + 1
			if "'Hello " + str(msgID) + "'" in row[2] or "'Hello " + str(msgID) + " " "from the client'" in row[2]:
				if 'recv' in row[2]:
					#print row[0], row[1], row[2]
					rece[msgID] = rece[msgID] + 1
				if 'send' in row[2]:
					#print row[0], row[1], row[2]
					send[msgID] = send[msgID] + 1

		#radio percentage
		if nodeID < 10:
			if "ID:" + str(nodeID) in row[1] and len(row[1]) == 4 and '(radio' in row[2]:
				print 'radio on time percentage:', row[1], row[2].split()[17]
				radioOn = radioOn + float(row[2].split()[17][:3])
				radioCount = radioCount + 1			
		else:
			if "ID:" + str(nodeID) in row[1] and '(radio' in row[2]:
				print 'radio on time percentage:', row[1], row[2].split()[17]
				radioOn = radioOn + float(row[2].split()[17][:3])
				radioCount = radioCount + 1	

	msgID = 0
	while msgID < numOfMsgs:
		msgID = msgID + 1
		r = float (rece[msgID]) / (send[msgID])
		r = round(r,4)
		print 'Hello ', msgID, ' recv:', rece[msgID], 'send:', send[msgID], 'packets delivery rate: ', r*100, '%'
		# Only count messages that have been sent 80 times
		if send[msgID] == 80:
			totalRecv = totalRecv + rece[msgID]
			totalSend = totalSend + send[msgID]
			count = count + 1

	print "Average radio on for node", nodeID, ": ", round((float(radioOn) / radioCount), 2), '%'		
	print "Average delivery rate (sending 80 times):", (float(totalRecv) / totalSend) * 100, '% ', "number of msgs", count  		
		
		
