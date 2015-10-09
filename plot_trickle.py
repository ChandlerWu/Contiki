#!/usr/bin/python
#!/usr/bin/env python
 
import csv
import matplotlib.pyplot as plt
 
# for P lines
#0-> str,
#1 -> clock_time(),2-> P, 3->rimeaddr_node_addr.u8[0],rimeaddr_node_addr.u8[1], 4-> seqno,
#5 -> all_cpu,6-> all_lpm,7-> all_transmit,8-> all_listen,9-> all_idle_transmit,10-> all_idle_listen,
#11->cpu,12-> lpm,13-> transmit,14-> listen, 15 ->idle_transmit, 16 -> idle_listen, [RADIO STATISTICS...]
 
 
from collections import defaultdict

def main():
	cpuOverTime =  defaultdict(list)
	i = 0
	s = 0

	f = file.open("failed one.txt")
	for line in f:
		rows = line.split(' ')
		for row in rows:
			i++
			print "Number of rows is ", len(rows)
			#print i, rows[0],rows[1],rows[2]
			if 'Consistent RX' not in rows[1]:
				if row[2] is 'P':
					cpuOverTime[row[3]].append(row[18][:-1])
					if i > 800:
						s = s + float(row[18][:-1])
						break

	print s / (i-800)
	 
	for i in cpuOverTime:
		plt.plot(cpuOverTime[i])
	plt.show()
########## 
