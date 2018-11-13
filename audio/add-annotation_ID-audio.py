import os
import re
import uuid
import pyclan as pc
from sets import Set
import sys


def randomID():
	randID = uuid.uuid4().hex[:6]
	while randID in usedID:
		randID = uuid.uuid4().hex[:6]
	usedID.add(randID)
	return randID

def replFunction(match):
	return match.group(0)+'_'+randomID()

# def processPhoLine(line):
# 	try:
# 		content = line.strip().split('\t', 1)[1].rstrip()
# 	except:
# 		return '%pho:\t_{}\n'.format(randomID())
# 	if(content.find('\t')>=0):
# 		phos = content.split('\t')
# 	else:
# 		phos = content.split(' ')
# 	phos = [pho+'_'+randomID() for pho in phos]
# 	return '%pho:\t'+'\t'.join(phos)+'\n'

# def processLine(line):
# 	if (line.startswith('%xcom') or line.startswith('%com')) and (line.count('|')<=3): #This is a usercomment
# 		return line.rstrip() + '####' + randomID() + '\n'
# 	elif line.startswith('%pho'): #This is a pho line
# 		return processPhoLine(line)
# 	else:
# 		return re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, line)

# def processFile(in_file, out_file):
# 	flattenedlines, breaks = pc.filters._preparse_flatten(in_file)
# 	for i in range(len(flattenedlines)):
# 		line = flattenedlines[i]
# 		if (line.startswith('%xcom') or line.startswith('%com')) and (line.count('|')<=3):
# 			flattenedlines[i] = flattenedlines[i].rstrip() + "####" + randomID() + '\n'
# 		elif line.startswith('%pho'):
# 			flattenedlines[i] = processPhoLine(line)
# 	with open(out_file, 'w') as f:
# 		for i in range(len(flattenedlines)):
# 			if len(breaks[i])>1:
# 				for j in range(len(breaks[i])-1):
# 					substr = flattenedlines[i][breaks[i][j]:breaks[i][j+1]]
# 					f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, substr) + '\n\t')
# 				substr = flattenedlines[i][breaks[i][-1]:]
# 				f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, substr))
# 			else:
# 				f.write(re.sub(r'&=[a-z]{1}_[a-z]{1}_[A-Z]{2}[A-Z0-9]{1}', replFunction, flattenedlines[i]))

def process_file(in_file, out_file):
	clan_file = pc.ClanFile(in_file)
	out = []
	for l in clan_file.line_map:
		matches = pc.code_regx.findall(l.line)
		new_line = l.line
		if len(matches)>0: 	# if there is an annotation on the line
			for match in matches: 	# for each annotation
				print(match, len(match))
				if match[-1]=='' and match[-2]=='':	# if there is no id for this annot
					# replace match by its ID-ed version
					print("adding")
					print(''.join(match))
					print(re.sub(''.join(match), ''.join(match)+'_'+randomID(), new_line))
					new_line = re.sub(''.join(match), replFunction, new_line)
					pass
				else:				# if there is an id for this annot
					pass			# do not change
		out.append(new_line)
	with open(out_file, 'w') as f:
		for l in out:
			f.write(l)


if __name__ == "__main__":

	input = sys.argv[1]

	if not input.endswith(".cha"):
		input_dir = input
		output_dir = sys.argv[2]
		usedIDFile = sys.argv[3]

		files = os.listdir(input_dir)
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
			if file.endswith('sparse_code.cha'):
				try:
					in_file = os.path.join(input_dir, file)
					out_file = os.path.join(output_dir, file)
					process_file(in_file, out_file)
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

	else:
		in_file = input
		if (len(sys.argv)>2):
			out_file = sys.argv[2]
		else:
			out_file = in_file
		# retrieve used id
		usedID = Set([])
		with open("used.txt") as f:
			for line in f.readlines():
				usedID.add(line.rstrip())

		# process file
		try:
			process_file(in_file, out_file)
		except Exception,e:
			print(file)
			print(e)

		# update used id
		with open("used.txt", 'a') as f:
			for id in usedID:
				f.write(id + '\n')
