import difflib
import os
import distance

originDir = '../../all_cha'
processedDir = './all_cha_with_id'

origin_files = [x for x in os.listdir(originDir) if x.endswith('.cha')]
processed_files = [x for x in os.listdir(processedDir) if x.endswith('.cha')]

files = sorted([x for x in origin_files if x in processed_files])

error_lines = []

def check_group(minus, plus, file):
	if len(minus)!=len(plus):
		print(minus)
		raise Exception("Length mismatch")
	for i in range(len(minus)):
		edit_distance = distance.levenshtein(minus[i].strip(), plus[i].strip())
		if edit_distance%10 != 0 and edit_distance%13 != 0:
			print(edit_distance)
			error_lines.append((file, minus[i].strip(), plus[i].strip()))
			print(error_lines[-1])

for file in files:
	print(file)
	with open(os.path.join(originDir, file)) as f:
		origin_file = f.readlines()
	with open(os.path.join(processedDir, file)) as f:
		processed_file = f.readlines()
	minus_group = []
	plus_group  = []
	diff = list(difflib.unified_diff(origin_file, processed_file, n=0))[2:]
	with open('diff.txt', 'w') as f:
		f.write('\n'.join(diff))
	idx = 0
	while idx < len(diff):
		entry = diff[idx]
		exception = False
		if entry.startswith('@@'):
			if len(entry.split()[1].split(','))==1:
				ran1 = 1
			else:
				ran1 = int(entry.split()[1].split(',')[1])
				if ran1==0:
					ran1 = 1
			if len(entry.split()[2].split(','))==1:
				ran2 = 1
			else:
				ran2 = int(entry.split()[2].split(',')[1])
				if ran2==0:
					ran2 = 1
			ran = max(ran1, ran2)

			for i in range(1, 2*ran+1):
				if diff[idx+i].startswith('-'):
					minus_group.append(diff[idx+i][1:])
				elif diff[idx+i].startswith('+'):
					plus_group.append(diff[idx+i][1:])
				else:
					error_lines.append((file, entry.strip(), ""))
					del minus_group[:]
					del plus_group[:]
					idx += i
					exception = True
					break
			if exception:
				continue
			idx += ran*2 + 1
		else:
			print(entry)
			raise Exception('Wrong idx increment')
		check_group(minus_group, plus_group, file)
		del minus_group[:]
		del plus_group[:]
	with open('error_lines.txt', 'w') as f:
		for error in error_lines:
			f.write('\t'.join(error)+'\n')