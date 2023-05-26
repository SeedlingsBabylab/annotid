require 'Datavyu_API'
require 'securerandom'

$inputDir = "~/Documents/Projects/Bergelson Lab/annotation/video_with_pho_output"
$outputDir = "~/Documents/Projects/Bergelson Lab/annotation/video_with_pho_with_ref"

def convertTime(time)
	ms = time%1000
	time/=1000
	sec = time%60
	time/=60
	mins = time%60
	time/=60
	hr = time
	return "#{hr}:#{mins}:#{sec}:#{ms}"
end

def addErrorFile(ambiguousFile, ambiguousLine, column)
	errorItem = Array.new
	for ind in ambiguousLine
		errorItem << column.cells[ind].object + "@" + convertTime(column.cells[ind].offset)
	end
	if $errorFile.has_key?(ambiguousFile)
		$errorFile[ambiguousFile] << errorItem
	else
		$errorFile[ambiguousFile] = Array.new
		$errorFile[ambiguousFile] << errorItem
	end
end

def addRef(dir, file, outDir)
	$db, $pj = load_db(File.join(dir, file))
   	column = get_column(get_column_list[0])
	column.add_code('reference')
	indexHash = Hash.new
	for ind in (0..column.cells.size-1) do
		cell = column.cells[ind]
		if indexHash.has_key?(cell.offset)
			indexHash[cell.offset] << ind
		else
			indexHash[cell.offset] = Array.new
			indexHash[cell.offset] << ind
		end
	end

	for key in indexHash.keys
		if indexHash[key].size<=1
			next
		elsif indexHash[key].size==2
	 		cellA = column.cells[indexHash[key][0]]
	 		cellB = column.cells[indexHash[key][1]]
	 		if !(cellA.object.start_with?('%pho')||cellB.object.start_with?('%pho'))
	 			next
	 		else
	 			if cellA.object.start_with?('%pho')
	 				cellA.reference = cellB.id
	 			else
	 				cellB.reference = cellA.id
	 			end
	 		end
		else
			#Count the number of cells starting with '%pho', if none does, then it is a trivial case
			counter = 0
			for ind in indexHash[key]
				if column.cells[ind].object.start_with?('%pho')
					counter += 1
				end
			end
			if counter>0
				addErrorFile(file, indexHash[key], column)
			end
		end
	end
   	set_column(column)
   	save_db(File.join(outDir, file))
end

begin
   	outDir = File.expand_path($outputDir)
	dataDir = File.expand_path($inputDir)
	files = Dir.new(dataDir).entries.sort
	counter = 0
	$errorFile = Hash.new
	for file in files
		if file.end_with? ('.opf')
			begin
				addRef(dataDir, file, outDir)
			rescue => error
				puts error
			end
		end
		counter += 1
		print("Finished: ", counter/(files.size.to_f)*100, "\n")
	end
	File.open(File.join(outDir, 'errorFile.txt'), 'w') { 
		|file| 
		for key in $errorFile.keys
			file.write(key + ":\n")
			for line in $errorFile[key]
				file.write("\t")
				file.write(line)
				file.write("\n")
			end
		end
	}
end
