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


numOfMsgs = 25

if len(sys.argv) == 2:
	numOfMsgs = int(sys.argv[1])
	#nodeID = int(sys.argv[2])
	print ""
	print "Number of message", numOfMsgs

nodeID = 12
msgLeft = True
msgID = 0
rece = [0] * (numOfMsgs + 1)
send = [0] * (numOfMsgs + 1)
radioOn = 0
radioCount = 0
totalSend = 0
numPackets = 0
numPkRece = 0
totalRecv = 0
count = 0
convergenceTime = ""
allRadioOnTime = 0
allRadioOnCount = 0
totalLatency = 0

receTime = [[0]*80 for i in range(0, numOfMsgs+1)]
sendTime = [[0]*80 for i in range(0, numOfMsgs+1)]




with open('test1.csv', 'rU') as f:
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		#Convergence time
		#I assume that the convergence time is the time last node sends 'hello 1'
		if "DATA send to 1 'Hello 1'" in row[2]:
			convergenceTime = row[0]

		#Latency
		#Average packets latency accorse all


		#Package delivery rate
		msgID = 0
		while msgID < numOfMsgs:
			msgID = msgID + 1
			if "'Hello " + str(msgID) + "'" in row[2] or "'Hello " + str(msgID) + " " "from the client'" in row[2]:
				if 'recv' in row[2]:
					#print row[0], row[1], row[2]
					rece[msgID] = rece[msgID] + 1
				
					#Get the time stamp of receiving
					receTime[msgID][int(row[2].split(' ')[8])-1] = row[0]

				if 'send' in row[2]:
					#print row[0], row[1], row[2]
					send[msgID] = send[msgID] + 1

 					#Get the time stamp of sending
					sendTime[msgID][int(row[1].split(':')[1])-1] = row[0]



		#Radio on time for all the nodes
		if '(radio' in row[2]:
			allRadioOnTime = allRadioOnTime + float(row[2].split()[17][:3])
			allRadioOnCount = allRadioOnCount + 1


		# #specific node radio percentage
		# if nodeID < 10:
		# 	if "ID:" + str(nodeID) in row[1] and len(row[1]) == 4 and '(radio' in row[2]:
		# 		print 'radio on time percentage:', row[1], row[2].split()[17]
		# 		radioOn = radioOn + float(row[2].split()[17][:3])
		# 		radioCount = radioCount + 1			
		# else:
		# 	if "ID:" + str(nodeID) in row[1] and '(radio' in row[2]:
		# 		print 'radio on time percentage:', row[1], row[2].split()[17]
		# 		radioOn = radioOn + float(row[2].split()[17][:3])
		# 		radioCount = radioCount + 1	

	msgID = 0
	while msgID < numOfMsgs:
		msgID = msgID + 1
		if send[msgID] is not 0:
			r = float (rece[msgID]) / (send[msgID])
			r = round(r,4)
			print 'Hello ', msgID, ' recv:', rece[msgID], 'send:', send[msgID], 'packets delivery rate: ', r*100, '%'
		#Get the total packets sent and receive
		numPkRece = numPkRece + rece[msgID]	
		numPackets = numPackets + send[msgID]

		#Calculate the latency time
		for i in range(0, 80):
			if receTime[msgID][i] is not 0:
				#Calculate the difference
				ts1 = receTime[msgID][i].replace(':','.').split(".")
				ts2 = sendTime[msgID][i].replace(':','.').split(".")
				diff1 = int(ts1[0]) - int(ts2[0])
				diff2 = int(ts1[1]) - int(ts2[1])
				diff3 = int(ts1[2]) - int(ts2[2])
				totalLatency = totalLatency + diff1*60 + diff2 + float(diff3)/10
			
				#print diff1*60 + diff2 + float(diff3)/10


		# Only count messages that have been sent 80 times
		if send[msgID] == 80:
			totalRecv = totalRecv + rece[msgID]
			totalSend = totalSend + send[msgID]
			count = count + 1


	print "Set up or convergence time:", convergenceTime
	print "Total packets sent:", numPackets		
	#print "Average radio on for node", nodeID, ": ", round((float(radioOn) / radioCount), 2), '%'
	print "Average radio on time for all nodes:", 	round((float(allRadioOnTime) / allRadioOnCount), 2), '%'
	print "Average latency:", round((float(totalLatency) / numPkRece), 2), "s"
	print "Average delivery rate (sending 80 times):", (float(totalRecv) / totalSend) * 100, '% '
	print "Number of msgs that have been sent 80 times:", count  		
		
		
