import os
import platform
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



def process_file(in_file, out_file):
	clan_file = pc.ClanFile(in_file)
	out = []
	for l in clan_file.line_map:
		matches = pc.code_regx.findall(l.line)
		new_line = l.line
		if len(matches)>0: 	# if there is an annotation on the line
			for match in matches: 	# for each annotation
				# print(match, len(match))
				if match[-1]=='' and match[-2]=='':	# if there is no id for this annot
					# replace match by its ID-ed version
					# print("adding")
					# print(''.join(match))
					# print(re.sub(''.join(match), ''.join(match)+'_'+randomID(), new_line))
					new_line = new_line.replace(''.join(match)+' ', ''.join(match)+'_0x'+randomID()+' ', 1)

					pass
				else:				# if there is an id for this annot
					pass			# do not change
		# print(new_line)
		out.append(new_line)
	with open(out_file, 'w') as f:
		for l in out:
			f.write(l)


if __name__ == "__main__":

	input = sys.argv[1]
	if platform.system() != "Windows":
		usedID_file = "/Volumes/pn-opus/Seedlings/usedID.txt"
	else:
		usedID_file = "Z:\\Seedlings\\usedID.txt"

	if not input.endswith(".cha"):
		input_dir = input
		output_dir = sys.argv[2]
		usedID_file = sys.argv[3]

		files = os.listdir(input_dir)
		files.sort()
		errorFiles = []
		counter = 0
		usedID = Set([])
		#Load used IDs to prevent collision
		with open(usedID_file) as f:
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

		with open(usedID_file, 'w') as f: # not 'a' because not adding (or will introduce duplicates, and size of file+++)
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
		with open(usedID_file) as f:
			for line in f.readlines():
				usedID.add(line.rstrip())

		# process file
		try:
			process_file(in_file, out_file)
		except Exception,e:
			print(file)
			print(e)

		# update used id
		with open(usedID_file, 'w') as f:
			for id in usedID:
				f.write(id + '\n')
