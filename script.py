import sys
from subprocess import Popen

'''
blastdb = Popen("makeblastdb -in " + sys.argv[2] + " -input_type fasta -dbtype nucl -out db.blastdb", shell=True)
blastdb.wait()

blastn = Popen("blastn -db db.blastdb -query " + sys.argv[1] + " -evalue 1e-20 -outfmt 6 -out resultado.txt", shell=True)
blastn.wait()
'''

query = []
subject = []
identityhits = []
with open("resultado.txt") as result:
	for line in result:
		select = line.split()
		query_ID = select[0]
		subject_ID = select[1]
		identity = select[2]
		
		query.append(query_ID)
		subject.append(subject_ID)
		identityhits.append(identity)

#Create dictionarie with all possible hits for some query ID
hits = {}
x = 0
while x < 100: #len(query):
	if query[x] not in hits:
		hits[query[x]] = []
		hits[query[x]].append(subject[x])
		hits[query[x]].append(identityhits[x])
	else:
		hits[query[x]].append(subject[x])
		hits[query[x]].append(identityhits[x])

	x += 1
	
#Select from the dictionarie the query, hits and identities
out_list = []
tophit = 0
count = 1
y = 0
for i in hits.items():
	geneID = i[0]
	list_maches = i[1]
	out_list.append([])
	for c in range(0, len(hits[query[y]]), 2):
		hits_ID = str(hits[query[y]][c])
		ident_hit = float(hits[query[y]][c+1])
		#Identify the hit with greater identity and it's ID
		if ident_hit > tophit:
			tophit_ID = hits_ID
			tophit = ident_hit
		elif ident_hit < tophit:
			tophit_ID = tophit_ID
			tophit = tophit

		out_list[0].append(hits_ID)
		
		y += 1
	out_list.append([])
	out_list[1].append(geneID)
	out_list.append([])
	out_list[2].append(tophit)
	out_list[2].append(tophit_ID)
	# Write the output file with the 4 colums
	file = f'./results/Out{count}.txt'
	with open(file, 'w') as output:
		output.write(''.join(out_list[1])+'\t'+', '.join(out_list[0])+'\t'+'\t'.join(map(str, out_list[2])))

	out_list.clear()
	tophit = 0
	count += 1
