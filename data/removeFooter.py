import requests
f = open("tytuly.txt")
my_list =  [line.rstrip('\n') for line in f]
for x in my_list:
	link = 'download/'+x+'.txt'
	plik0=open(link,'r')
	fileName = 'changed/'+x+'.txt'
	file1 = open(fileName, 'w')
	docs = plik0.readlines()
	for i in range(0, len(docs)-13):
		file1.write(docs[i])
	file1.close()
