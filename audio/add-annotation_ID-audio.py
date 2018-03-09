import os
import re
import uuid
import pyclan as pc
from sets import Set
import sys

inputDir = "/Users/estellehe/Documents/BLAB/workspace/clan/audio"
#inputDir = "./"
outputDir = "/Users/estellehe/Documents/BLAB/workspace/clan/audioid"
usedIDFile = "/Users/estellehe/Documents/BLAB/workspace/clan/usedID.txt"

def randomID():
	randID = uuid.uuid4().hex[:9]
	while randID in usedID:
		randID = uuid.uuid4().hex[:9]
	usedID.add(randID)
	return randID

def replFunction(match):
	return match.group(0)+'_'+randomID()

def processPhoLine(line):
	try:
		content = line.strip().split('\t', 1)[1].rstrip()
	except:
		return '%pho:\t_{}\n'.format(randomID())
	if(content.find('\t')>=0):
		phos = content.split('\t')
	else:
		phos = content.split(' ')
	phos = [pho+'_'+randomID() for pho in phos]
	return '%pho:\t'+'\t'.join(phos)+'\n'

def processLine(line):
	if (line.startswith('%xcom') or line.startswith('%com')) and (line.count('|')<=3): #This is a usercomment
		return line.rstrip() + '####' + randomID() + '\n'
	elif line.startswith('%pho'): #This is a pho line
		return processPhoLine(line)
	else:
		return re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, line)

def processFile(file):
	flattenedlines, breaks = pc.filters._preparse_flatten(os.path.join(inputDir, file))
	for i in range(len(flattenedlines)):
		line = flattenedlines[i]
		if (line.startswith('%xcom') or line.startswith('%com')) and (line.count('|')<=3):
			flattenedlines[i] = flattenedlines[i].rstrip() + "####" + randomID() + '\n'
		elif line.startswith('%pho'):
			flattenedlines[i] = processPhoLine(line)
	with open(os.path.join(outputDir, file), 'w') as f:
		for i in range(len(flattenedlines)):
			if len(breaks[i])>1:
				for j in range(len(breaks[i])-1):
					substr = flattenedlines[i][breaks[i][j]:breaks[i][j+1]]
					f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, substr) + '\n\t')
				substr = flattenedlines[i][breaks[i][-1]:]
				f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, substr))
			else:
				f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, flattenedlines[i]))

files = os.listdir(inputDir)
files.sort()
errorFiles = []
counter = 0
usedID = Set([])
#Load used IDs to prevent collision
with open(usedIDFile) as f:
	for line in f.readlines():
		usedID.add(line.rstrip())

if '--fix-error' in sys.argv: #Only process files with error
	files = []
	with open('add-annotation_ID-error-file.txt') as f:
		for line in f.readlines():
			files.append(line.rstrip().strip('\''))

for file in files:
	if file.endswith('.cha'):
		try:
			processFile(file)
		except Exception,e:
			print(e)
			errorFiles.append(file)
	counter += 1
	print("Finished: {}".format(counter/float(len(files))*100))

with open(usedIDFile, 'a') as f:
	for id in usedID:
		f.write(id + '\n')

print('Had problems processing the following files:')
print(errorFiles)
