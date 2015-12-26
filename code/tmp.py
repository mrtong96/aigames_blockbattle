
f = open('test_output.txt', 'r').read()
f = f.split('\n')

times_taken = []
nodes_expanded = []
no_path_counter = 0

for line in f:
	if 'time taken' in line:
		line = line[line.index('time taken'):]
		line = line[len('time taken: '):]
		
		times_taken.append(float(line))
	

	if 'nodes expanded' in line:
		line = line[line.index('nodes expanded'):]
		line = line[len('nodes expanded: '):]

		nodes_expanded.append(float(line))

	if ':no path:' in line:
		no_path_counter += 1

print sum(times_taken)
print len(times_taken)
avg = sum(times_taken) / len(times_taken)
print avg
sum_sq_diff = sum(map(lambda x: (x - avg) ** 2, times_taken))
print (sum_sq_diff / len(times_taken)) ** .5 


print '------'
print sum(nodes_expanded)
print len(nodes_expanded)
avg = sum(nodes_expanded) / len(nodes_expanded)
print avg
sum_sq_diff = sum(map(lambda x: (x - avg) ** 2, nodes_expanded))
print (sum_sq_diff / len(nodes_expanded)) ** .5 

print '------'
print no_path_counter
print max(times_taken)
times_taken.sort()

print times_taken


'''
Data:
	depth 1:
		n = 	64
		mean = 	29.25
		sd =	15.38

'''