import os
import re
import uuid
import pyclan as pc
from sets import Set
import sys

inputDir = "./audio"
#inputDir = "./"
outputDir = "./audioOutput"
usedIDFile = "./usedID.txt"

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
		return '%pho:\t\n'
	if(content.find('\t')>=0):
		phos = content.split('\t')
	else:
		phos = content.split(' ')
	phos = [pho+'_'+randomID() for pho in phos]
	return '%pho:\t'+'\t'.join(phos)+'\n'

def processLine(line):
	if line.startswith('%xcom'): #This is a usercomment
		return line.rstrip() + '####' + randomID() + '\n'
	elif line.startswith('%pho'): #This is a pho line
		return processPhoLine(line)
	else:
		return re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Za-z]{3}', replFunction, line)

def processFile(file):
	clan_file = pc.ClanFile(os.path.join(inputDir, file))
	clan_file.flatten()
	for line in clan_file.line_map:
		line.line = processLine(line.line)
	clan_file.write_to_cha(os.path.join(outputDir, file))

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
		except:
			errorFiles.append(file)
	counter += 1
	print("Finished: {}".format(counter/float(len(files))*100))

with open(usedIDFile, 'a') as f:
	for id in usedID:
		f.write(id + '\n')

print('Had problems processing the following files:')
print(errorFiles)