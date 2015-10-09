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
cpuOverTime =  defaultdict(list)
i = 0
s = 0
 
with open('failed one.txt', 'rb') as f:
	reader = csv.reader(f,delimiter=' ')
	for row in reader:
		i = i + 1
		#print i, row[0],row[1],row[2]
		if 'Consistent RX' not in row[1]:
			if row[2] is 'P':
				cpuOverTime[row[3]].append(row[18][:-1])
				if i > 800:
					s = s + float(row[18][:-1])

print s/ (i-800)
 
for i in cpuOverTime:
	plt.plot(cpuOverTime[i])
plt.show()
########## 
