import requests
#from pprint import pprint
import operator

f = open("tytuly.txt")
my_list =  [line.rstrip('\n') for line in f]
iloscDzielAutora = {}
for x in my_list:
	link = 'changed/'+x+'.txt'
	plik0=open(link,'r')
	#fileName = 'changed/'+x+'.txt'
	#file1 = open(fileName, 'w')
	docs = plik0.readlines()
	#print(link)
	if (len(docs) > 0 ):
		#print(docs[0])
		if (docs[0] in iloscDzielAutora ):
			iloscDzielAutora[docs[0]] =iloscDzielAutora[docs[0]] +1
		else:
			iloscDzielAutora[docs[0]] = 1
	#for i in range(0, len(docs)-13):
	#	file1.write(docs[i])
	#file1.close()
#for item in sorted(iloscDzielAutora):
#	print(item)
#	print(iloscDzielAutora[item])
#pprint(iloscDzielAutora)

#for key, value in sorted(iloscDzielAutora.items()):
#	print("{} : {}".format(key, value))

for key, value in sorted(iloscDzielAutora.items(), key=operator.itemgetter(1)):
	print("{} : {}".format(key, value))
