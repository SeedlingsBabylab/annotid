require 'Datavyu_API'

# the script will check all the opf file in the directory recursively
opf_folder = "/Users/estellehe/Documents/GitHub/annotid/video/output/"
pattern = /^0x[0-9a-z]{6}$/
usedID_file = "/Volumes/pn-opus/Seedlings/usedID.txt"

begin
  usedID = []
  File.open(usedID_file, "rb") do |f|
    f.each_line do |line|
      usedID << line.strip
    end
  end

  error = Array.new
  for opf in Dir[File.join(opf_folder, "**", "*.opf")] do
    $db,$pj = load_db(opf)
    col = getColumn("labeled_object")
    cells = col.cells
    for cell in col.cells do
      id = cell.get_code("id")
      if (pattern =~ id).nil?
        error << [opf, cell.get_codes(), "missing ID"]
      elsif not usedID.include? (id)
        error << [opf, cell.get_codes(), "ID not in usedID"]
      end
    end
  end

  CSV.open(File.join(opf_folder, "error_summary.csv"), "wb") do |csv|
    csv << ["file name", "line", "error type"]
    for e in error do
      csv << e
    end
  end
end
