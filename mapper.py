import sys

# def openfile():
# 	"Opening input file"
# 	file_name = sys.argv[1]
# 	minsupport = int(sys.argv[2])
# 	nbuckets=int(sys.argv[3])
# 	f = open("map_out.txt", "a")
# 	f.write(str(minsupport))
# 	f.write("\n")
# 	f.write(str(nbuckets))
# 	f.write("\n")
# 	f.close()
# 	"Reading input file"
# 	doc = open(file_name).read()
# 	"Removing newline characters"
# 	newfile=doc.split()
# 	"Creating buckets"
# 	buckets=[]
# 	for x in newfile:
# 		buckets.append(x.split(','))
# 	size1freqset(minsupport,nbuckets,buckets);

def openfile(buckets):
	minsupport = 2
	nbuckets = 5
	f = open("map_out.txt", "a")
	f.write(str(minsupport))
	f.write("\n")
	f.write(str(nbuckets))
	f.write("\n")
	f.close()
	size1freqset(minsupport,nbuckets,buckets);

def size1freqset(minsupport,nbuckets,buckets):
	"Creating Candidate List of Size 1"
	candidatelist1=[]
	finalist1=[]
	
	for i in range(0, len(buckets)):
		for b in buckets[i]:
			candidatelist1.append(b)

	candidatelist1=sorted(set(candidatelist1))
	# print(candidatelist1)

	"Appending frequent items of size 1 to finallist1"
	lala=0
	for k in candidatelist1:
		for i in range(0, len(buckets)):
			for j in buckets[i]:
				if(k==j):
					lala+=1
		if lala>=minsupport:
			finalist1.append(k)
		lala=0

	itemiddic={}
	counter=1
	for c in candidatelist1:
		itemiddic[c]=counter
		counter+=1
	f = open("map_out.txt", "a")
	f.write(str(itemiddic))
	print(itemiddic)
	f.write("\n")
	f.close()
	if finalist1:
		print("Frequent Itemsets of size 1")
		for x in finalist1:
			print(x)
		size2freqset(minsupport,nbuckets,itemiddic,buckets,finalist1);
	else:
		print("That's all folks!")

def size2freqset(minsupport,nbuckets,itemiddic,buckets,finalist1):
	k=3
	countofbuckets=[0]*nbuckets
	bitmap=[0]*nbuckets
	pairs=[]
	"PCY Pass 1"
	for i in range(0,len(buckets)):
		for x in range(0,len(buckets[i])-1):
			for y in range(x+1,len(buckets[i])):
				if(buckets[i][x]<buckets[i][y]):
					countofbuckets[int(str(itemiddic[buckets[i][x]])+str(itemiddic[buckets[i][y]]))%nbuckets]+=1
					if ([buckets[i][x],buckets[i][y]] not in pairs):
						pairs.append(sorted([buckets[i][x],buckets[i][y]]))
				else:
					countofbuckets[int(str(itemiddic[buckets[i][y]])+str(itemiddic[buckets[i][x]]))%nbuckets]+=1
					if ([buckets[i][y],buckets[i][x]] not in pairs):
						pairs.append(sorted([buckets[i][y],buckets[i][x]]))

	pairs=sorted(pairs)
	for x in range(0,len(countofbuckets)):
		if countofbuckets[x]>=minsupport:
			bitmap[x]=1
		else:
			bitmap[x]=0
	prunedpairs=[]

	"Checking condition 1 of PCY Pass 2"

	for i in range(0,len(pairs)):
		for j in range(0,len(pairs[i])-1):
			if(pairs[i][j] in finalist1 and pairs[i][j+1] in finalist1):
				prunedpairs.append(pairs[i])

	# for f in prunedpairs:
	# 	print(f)

	candidatelist2=[]

	"Checking condition 2 of PCY Pass 2"
	for i in range(0, len(prunedpairs)):
		for j in range(0,len(prunedpairs[i])-1):
			if bitmap[int(str(itemiddic[prunedpairs[i][j]])+str(itemiddic[prunedpairs[i][j+1]]))%nbuckets]==1:
				candidatelist2.append(prunedpairs[i])

	# for p in candidatelist2:
	# 	print(p)

	"Appending frequent items of size 2 to finallist2"
	finalist2=[]
	p=0
	for c in range(0,len(candidatelist2)):
		for b in range(0,len(buckets)):	
			if set(candidatelist2[c]).issubset(set(buckets[b])):
				p+=1
		if p>=minsupport and p!=0:
			finalist2.append(sorted(candidatelist2[c]))
		p=0

	finalist2=sorted(finalist2)
	
	if finalist2:
		f = open("map_out.txt", "a")
		print("\nFrequent Itemsets of size 2")
		for b in finalist2:
			print((','.join(b)))
			f.write(','.join(b))
			f.write("\n")
		# sizekfreqset(minsupport,nbuckets,itemiddic,buckets,finalist2,k);
		f.close()
	else:
		print("Starting Reducer...")

if __name__ == "__main__":
	print("Starting Mapper...")
	buckets = []
	for x in sys.stdin:
		buckets.append(x.rstrip("\n").split(','))
	print(buckets)
	openfile(buckets)
