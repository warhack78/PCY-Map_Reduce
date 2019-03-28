import sys, ast

def sizekfreqset(minsupport,nbuckets,itemiddic,buckets,prevout,k):
	"Creating Candidate List of Size k"
	kcountofbuckets=[0]*nbuckets
	kbitmap=[0]*nbuckets
	kcombination=[]
	prevout=prevout
	"Make k combination e.g. triplets"
	for a in prevout:
		for b in prevout:
			if(a!=b):
				if set(a) & set(b) and len(list(set(a) & set(b))) >= k-2:
					kcombination.append(sorted(set(a)|set(b)))
	# print(kcombination)

	# print("checking kcombination")
	kcombination=sorted(kcombination)
	"PCY Pass 1 Hashing"
	hashingstring=""
	for i in range(0,len(kcombination)):
		for x in kcombination[i]:
			hashingstring+=str(itemiddic[x])
		kcountofbuckets[int(hashingstring)%nbuckets]+=1
		hashingstring=""

	for x in range(0,len(kcountofbuckets)):
		if kcountofbuckets[x]>=minsupport:
			kbitmap[x]=1
		else:
			kbitmap[x]=0

	"Condition 1 is automatically satisfied"
	"Checking condition 2 of PCY Pass 2"
	hashingstring=""
	klist=[]
	for i in range(0, len(kcombination)):
		for j in kcombination[i]:
			hashingstring+=str(itemiddic[j])
		if kbitmap[int(hashingstring)%nbuckets]==1:
			klist.append(kcombination[i])
		teststring=""

	"Creating Candidate List of Size k"
	candidatelistk=[]
	count=1
	for i in range(1, len(klist)):
		if klist[i]==klist[i-1]:
			count+=1
		else:
			# print("ELement is: ",klist[i-1]," and count is: ",count)
			if count>=k:
				candidatelistk.append(klist[i-1])
			count=1
	if count>=k:
		candidatelistk.append(klist[i-1])
		# print("ELement is: ",klist[i-1]," and count is: ",count)
	
	"Appending frequent items of size k to output"
	output=[]
	counter=0
	for c in range(0,len(candidatelistk)):
		for b in range(0,len(buckets)):
			if set(candidatelistk[c]).issubset(set(buckets[b])):
				counter+=1
		if counter>=minsupport and counter!=0:
			output.append(candidatelistk[c])
		counter=0

	if output:
		f = open("reducer_out.txt", "w")
		print("\nFrequent Itemsets of size ",k)
		for b in output:
			f.write(','.join(b))
			f.write("\n")
		k+=1
		f.close
		sizekfreqset(minsupport,nbuckets,itemiddic,buckets,output,k);
		# print("\n")
	else:
		print("")

if __name__ == "__main__":
	print("Reducer Started...")
	k = 3
	data = []
	for line in sys.stdin:
		data.append(line)
	# print(int(data[0]))
	minsupport = int(data[0])
	nbuckets = int(data[1])
	# print(minsupport, nbuckets)
	itemiddic = ast.literal_eval(data[2])
	doc = open("map_out.txt").read()
	newfile=doc.split()
	finalist2 = data[3:]
	# for x in newfile:
	# 	finalist2.append(x.split(','))
	# print(buckets)
	# del finalist2[:(len(itemiddic)+13)]
	print(finalist2)
	"Reading input file"
	doc = open("input.txt").read()
	"Removing newline characters"
	newfile=doc.split()
	"Creating buckets"
	buckets=[]
	for x in newfile:
		buckets.append(x.split(','))
	# print(buckets)
	sizekfreqset(minsupport,nbuckets,itemiddic,buckets,finalist2,k);