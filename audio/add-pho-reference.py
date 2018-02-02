import os
import re
import uuid
import sys
import pyclan as pc
from sets import Set
from itertools import groupby

inputDir = "./audioOutput"
outputDir = "./audio_output_with_ref"

class ChaFileError(Exception):
    def __init__(self, message, errors):
        super(ChaFileError, self).__init__(message)
        self.errors = errors

class LineNumberMismatchError(Exception):
    def __init__(self, message, errors):
        super(LineNumberMismatchError, self).__init__(message)
        self.errors = errors

class SpaceDelimiterError(Exception):
    def __init__(self, message, errors):
        super(SpaceDelimiterError, self).__init__(message)
        self.errors = errors

def convertTime(time):
	ms = time%1000
	time/=1000
	sec = time%60
	time/=60
	mins = time%60
	time/=60
	hr = time
	return "{}:{}:{}:{}".format(hr, mins, sec, ms)

def notSoIntelligentMatching(file, phos, chis):
	chiToPhoMapping = {}
	phoToChiMapping = {}
	phoLineMap = {}
	chiLineMap = {}
	for chi in chis:
		chiToPhoMapping[chi] = None
		if not chi.line_num in chiLineMap:
			chiLineMap[chi.line_num] = []
		chiLineMap[chi.line_num].append(chi)
	for pho in phos:
		phoToChiMapping[tuple(pho)] = None
		if not pho[1] in phoLineMap:
			phoLineMap[pho[1]] = []
		phoLineMap[pho[1]].append(pho)
	for chi in chis:
		if chiToPhoMapping[chi]: #already matched
			pass
		else:
			for i in range(3): # +- 2 lines
				lineNum = chi.line_num + i
				if lineNum in phoLineMap:
					matched = False
					for pho in phoLineMap[lineNum]:
						if not phoToChiMapping[tuple(pho)]:
							phoToChiMapping[tuple(pho)] = chi
							chiToPhoMapping[chi] = phoLineMap[lineNum]
							matched = True
							break
					if matched:
						break

	noMatchChi = []
	noMatchPho = []
	for key in chiToPhoMapping.keys():
		if not chiToPhoMapping[key]:
			noMatchChi.append((convertTime(key.onset), key.orig_string))
	for key in phoToChiMapping.keys():
		if not phoToChiMapping[tuple(key)]:
			noMatchPho.append((convertTime(key[2]), key[0]))
	return noMatchChi, noMatchPho

def processFile(file):
	clan_file = pc.ClanFile(os.path.join(inputDir, file))
	clan_file.flatten()
	clan_file.reindex()
	clan_file.annotate()
	phos = [x for x in clan_file.line_map if x.line.startswith("%pho:")]
	chis = [x for x in clan_file.annotations() if x.speaker == "CHI"]
	sorted_phos = sorted(list(set(phos)), key=lambda x: x.index) #This sorting might be unnecessary
	phos = []

	spaceDelimiterLineOnset = []
	for pho in sorted_phos:
		try:
			results = pho.content.translate(None, '\r\n').split('\t')
			if pho.content.translate(None, '\r\n').find(' ') >= 0:
				raise SpaceDelimiterError('Found space delimited %pho line', convertTime(pho.onset))
			#Keep track on the line number as well as the content
		except SpaceDelimiterError, e:
			spaceDelimiterLineOnset.append(e.errors)
			results = pho.content.translate(None, '\r\n').split(' ')
		finally:
			for result in results:
				if result:
					phos.append([result, pho.index, pho.onset])

	if len(phos) != len(chis):
		raise LineNumberMismatchError('Mismatch number of %pho and CHI', (phos, chis))
	else:
		for idx in range(len(chis)):
			chi_ref = chis[idx].annotation_id
			phos[idx][0] += '_' + chi_ref

	for lineIndex, group in groupby(phos, lambda x: x[1]):
		clan_file.line_map[lineIndex].line = '%pho:\t' + '\t'.join([x[0] for x in group]) + '\n'

	clan_file.write_to_cha(os.path.join(outputDir, file))
	if spaceDelimiterLineOnset:
		raise ChaFileError('Space Delimited %pho Error', (file, spaceDelimiterLineOnset))

files = os.listdir(inputDir)
files.sort()
counter = 0

errorFile = open('audio_pho_ref_error.txt', 'w')


if '--fix-error' in sys.argv: #Only process files with error
	files = []
	with open('add-pho-reference-error-file.txt') as f:
		for line in f.readlines():
			files.append(line.rstrip().strip('\''))

for file in files:
	print file
	if file.endswith('.cha'):
		try:
			processFile(file)
		except Exception, e:
			if isinstance(e, ChaFileError):
				errorFile.write(e.errors[0]+': '+'\n')
				errorFile.write('\t'+e.message+'\n')
				errorFile.wrtie('\t\t')
				errorFile.write('\n\t\t'.join(e.errors[1]))
				errorFile.write('\n')
				errorFile.flush()
			if isinstance(e, LineNumberMismatchError):
				noMatchChi, noMatchPho = notSoIntelligentMatching(file, e.errors[0], e.errors[1])
				errorFile.write(file+': \n')
				errorFile.write('\t'+e.message + '\n\t\t')
				errorFile.write('\n\t\t'.join([x[1]+'@'+x[0] for x in noMatchChi]))
				errorFile.write('\n\t\t')
				errorFile.write('\n\t\t'.join([x[1]+'@'+x[0] for x in noMatchPho]))
				errorFile.write('\n')
				errorFile.flush()
			else:
				print e
	counter += 1
	print("Finished: {}".format(counter/float(len(files))*100))
errorFile.close()