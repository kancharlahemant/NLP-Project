#!/usr/bin/python
import nltk,math,sys
#stopwords=['i','in','a','an','is','the','of','there','by','are','u','and','am','that',',','.','?']
stopwords=[]
dist_spam=0
dist_ham=0
nspam=0
nham=0
spam=0
ham=0
word_spam={}
word_ham={}
v=50000
def stop():
	global stopwords
	f2=open("stop.txt","r")
	for line in f2:
		line=line.replace("\r\n","")
		stopwords.append(line)

def train(fname):
	global ham,spam,word_spam,word_ham,nspam,nham,dist_spam,dist_ham,stopwords
	f=open(fname,"r")
	for line in f:
		line=line[:-1]
		#---LOWER CASE
		line=line.lower()
		a=line.split('\t')[0]
		line=line.replace(a+'\t','')
		words=nltk.word_tokenize(line)
		if a.lower()=="ham":
			ham+=1
			for word in words:
				if word not in stopwords:
					#	word=word.replace("...","")
			#		word=word.replace("..","")
			#		word=word.replace(".","")
					nham+=1
					try:
						word_ham[word]+=1
					except:
						dist_ham+=1
						word_ham[word]=1
		else:
			spam+=1
			for word in words:
				if word not in stopwords:
					nspam+=1
					try:
						word_spam[word]+=1
					except:
						dist_spam+=1
						word_spam[word]=1


def test(s):
	global ham,spam,word_spam,word_ham,nspam,nham,dist_spam,dist_ham
	pham=ham*1.0/(spam+ham)
	pspam=spam*1.0/(spam+ham)
	words=nltk.word_tokenize(s)
	for word in words:
		try:
			pspam*=(word_spam[word]+1)*1.0/(v+nspam)
		except:
			pspam*=1.0/(nspam+v)
		try:
			pham*=(word_ham[word]+1)*1.0/(v+nham)
		except:
			pham*=1.0/(nham+v)
	#print pham,pspam
	if pham>=pspam:
		return 1
	else:
		return 0





if len(sys.argv)<2:
	print "PLEASE GIVE COMMAND LINE ARGUEMENTS"
	sys.exit(0)
stop()
#print stopwords
train(sys.argv[1])
#print word_ham
'''
f1="GET a mobile Free of cost"
print test(f1)

for word in word_ham.keys():
	if word_ham[word]==1:
		#print word
		nham-=word_ham[word]
		del word_ham[word]

for word in word_spam.keys():
	if word_spam[word]==1:
		#print word
		nspam-=word_spam[word]
		del word_spam[word]
		
'''
f1=open(sys.argv[2],"r")
total=0
same_spam=0
same_ham=0
tspam=0
tham=0
same=0
for line in f1:
	total+=1
	line=line[:-1]
	line=line.split('\t')
	if line[0]=="ham":
		tham+=1
	else:
		tspam+=1
	if len(line)<2:
		continue
	if test(line[1].lower())==1:
		print "ham\t",line[1]
		if line[0]=="ham":
			same+=1
			same_ham+=1
	else:
		print "spam\t",line[1]
		if line[0]=="spam":
			same+=1
			same_spam+=1

accuracy=same*100.0/total
print "precision = ",accuracy
print "spam recall = ",same_spam*100.0/(tspam)
print "ham recall = ",same_ham*100.0/(tham)
#print tham,tspam
#print same_ham,same_spam

