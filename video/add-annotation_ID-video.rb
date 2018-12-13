require 'Datavyu_API'
require 'securerandom'

# $inputDir = "~/Documents/Projects/Bergelson Lab/annotation/video_with_pho"
# $outputDir = "~/Documents/Projects/Bergelson Lab/annotation/video_with_pho_output"

$inputDir = "/Volumes/pn-opus/Seedlings/Working_Files/annot_id/video/full_files/"
$outputDir = "/Volumes/pn-opus/Seedlings/Working_Files/annot_id/video/output/"
$usedIDFile = "/Volumes/pn-opus/Seedlings/Working_Files/annot_id/video/usedID.txt"

def randomID
	randID = SecureRandom.uuid
	randID = randID[0..5]
	while($usedID.include?(randID))
		p "ID Collision"
		randID = SecureRandom.uuid
		randID = randID[0..5]
	end
	$usedID << randID
	return randID
end

def printCode(*code)
	columnName = get_column_list[0]
   	theColumn = get_column(columnName)
   	for cell in theColumn.cells
   		p cell.get_codes(code)
   	end
end

def addID(dir, file, outDir)
	$db, $pj = load_db(File.join(dir, file))
   	columnName = get_column_list[0]
   	theColumn = get_column(columnName)
		unless theColumn.arglist.include? "id"
   		theColumn.add_code('id')
		end
   	for cell in theColumn.cells
			if cell.get_code('id').to_s.strip.nil? || cell.get_code('id').to_s.strip.empty?
				p cell.get_code('id')
   			cell.change_code('id', randomID)
			end
   	end
   	set_column(theColumn)
   	save_db(File.join(outDir, file))
end

begin
	outDir = File.expand_path($outputDir)
	dataDir = File.expand_path($inputDir)
	# retrieve used IDs
	$usedID = Set.new
	fID = open $usedIDFile
	fID.each do |line|
		$usedID << line
	end
	files = Dir.new(dataDir).entries.sort
	counter = 0
	errorFile = Array.new
	for file in files
		if file.end_with? ('.opf')
			begin
				puts file
				addID(dataDir, file, outDir)
			rescue
				errorFile << file
				print("Error with file: ", file, "\n")
			end
		end
		counter += 1
		print("Finished: ", counter/(files.size.to_f-2)*100, "\n")
	end
	# File.open(File.join(outDir, 'usedID.txt'), 'w') {
	File.open($usedIDFile, 'w') {
		|file|
		for id in $usedID
			file.write(id + "\n")
		end
	}
	print("Had problem with: \n")
	p errorFile
end
