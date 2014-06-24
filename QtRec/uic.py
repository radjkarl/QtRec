


def insertRec(catchprase, inputfilename, outputfilename=None):
	'''
	xxxxxxxx
	'''
	# read file, write in to 'content'
	with open(inputfilename,'r') as f:
		content = f.readlines()
		
	#insert QtRec.QtGui import under normal QtGui import:
	for n,line in enumerate(content):
		if 'import' in line and 'QtGui' in line:
			content.insert(n+1,'from QtRec import QtGui as QtRecGui')
			break

	# for each line
	for n,line in enumerate(content):
	# rename the first 'QtGui' into 'QtRecGui if...
	#     the line starts with 'self'
	#     '=' is in line
	#     between 'self' and '=' the catchphrase appears
		i = line.find('self')
		if i and '=' in line and line[:i].isspace():
			i = line.index('=')
			left_side = line[:i]
			if catchprase in left_side:
				right_side = line[i:].replace('QtGui', 'QtRecGui', 1) #replace the first occurence
				content[n] = left_side + right_side


	if not outputfilename:
		outputfilename = inputfilename
	# write output file
	with open(outputfilename,'w') as f:
		f.writelines(content)

	print("Created/Modified file '%s' for QtRec support." %outputfilename)


def removeRec(self):
	raise NotImplemented()
