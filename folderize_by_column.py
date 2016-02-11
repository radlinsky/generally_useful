#!/usr/bin/python

### folderize_by_column.py
### Caleb Matthew Radens
### 2015_2_10

### This script parses a file by a specified column, and writes to
###  file groups of rows that match into their own folders. 
###  Files are named by their row group. 
###
###	Arguments:
###		input_file.txt: input txt file
###			valid filepath   
###		delim: how is input file delimted?
###		head: Is there a single-lined header?
###			integer (0 or 1)
###		Column_#: which column to group by
###			integer
###		Sort_style: 'n' if column is numeric. 's' if column is string.
###		output_directory/: where should files by written to?
###			Extant directory
###		keep_*: which columns from the file to keep (order matters) when writing new files.
###			keep_all = keep all columns in new files
###			keep_0_1_2 = keep first 3 columns in new files
###			keep_6_2_4 = keep the 7th, 3rd, and 5th columns..
###			NOTE: preserves order of input file if 'all' or order of input columns, if specified
###
###	Assumptions:
###		The file is bash-sortable by the column of interest
###		The 'Column_#' command line argument is a valid column index
###			Type = <int>
###			(0 = first column)
###		The column of interest has no empty values
###		The column of interest does not have any rows with value='INITIATED'
###		The file is not zipped/compressed
###		The file is a .txt file
###		There is a single line header or no header at all
###
###	Usage:
###		python folderize_by_gene.py input_file.txt delim head Column_# sort_style output_directory/ keep_*

import sys
import os
import csv
from subprocess import call

print "Initiating folderize_by_column.py"
print "Argument List:", str(sys.argv[1:])

if (len(sys.argv)-1 != 7):
	raise Exception("Expected seven command arguments.")
in_FILE = str(sys.argv[1])
delim = str(sys.argv[2])
head = int(sys.argv[3])
Column_index = int(sys.argv[4])
sort_style = str(sys.argv[5])
out_DIR = str(sys.argv[6])
Keep = str(sys.argv[7])

if (in_FILE[-4:] != ".txt"):
	raise Exception("Expected 1st command argument to be a file name ending in '.txt'")
if not (os.path.isfile(in_FILE)):
	raise ValueError(in_FILE+" not found. Is it a *full* and valid file path?")
# from bash, >>> python \t sends a 't' to python. >>> python $'\t' sends \t.
#    this little check assumes user meant \t
if "t" in delim and len(delim)==1:
	delim = "\t"
if head != 0 and head != 1:
	raise ValueError("head needs to be integer: 0 or 1. Not: "+str(head))
if not type(Column_index) is int or Column_index < 0:
	raise Exception("Column index needs to be an integer >= 0.")
if type(sort_style) is not str:
	raise TypeError("sort_style needs to be a string")
if sort_style != "n" and sort_style != "s":
	raise ValueError("sort_style needs to be 'n' or 's', not: "+sort_style)
if not (os.path.isdir(out_DIR)):
	raise ValueError(out_DIR+" not found. Is it a valid directory?")
if out_DIR[-1] != "/":
	raise ValueError("The out directory needs to end with a forward slash.")
if not "keep_" in Keep:
	raise ValueError("'keep_*' argument needs to start with 'keep_'")
after_keep = Keep[len("keep_"):]
if len(after_keep) == 0:
	raise ValueError("Please specify 'all' or 'col#_col#_etc' after 'keep_'. Saw: "+after_keep)
if "all" in after_keep:
	if any(char.isdigit() for char in after_keep):
		raise ValueError("Please only choose one: 'all' or 'col#_col#_etc' after 'keep_'")
	if len(after_keep[len("all"):]) > 0:
		raise ValueError("Expected nothing after 'keep_all' but saw: keep_all"+after_keep)
	# Temporarily make cols_to_keep = "all" (it will be over-written later)
	cols_to_keep = "all"
# Note:
#	any(char.isdigit() for char in STRING_OF_INTEREST)
#	This checks if there are any digits in the STRING_OF_INTEREST
elif any(char.isdigit() for char in after_keep):
	split_keep = after_keep.split("_")
	cols_to_keep = list()
	for keep_col in split_keep:
		if not keep_col.isdigit:
			raise ValueError("Expected 'keep_#_#...', but instead of #, saw: "+keep_col)
		cols_to_keep.append(int(keep_col))
else:
	raise ValueError("'keep_*' argument isn't properly formatted. Looked like: "+Keep)
		
print "Passed script checks."
print "Keeping column(s): "+str(cols_to_keep)

def bash_sort(File, In_dir, Out_dir, Col, Delim = "\\t", Sort_style="", Header = True):
	""" Bash sort a file, return location of sorted file.

		Arguments:
			File: 		"my_fav_file.txt"
			In_dir: 	"/my_directory/" [optional, you may make File a the full filepath instead
			Out_dir:	"/some_dir" where sorted file is saved
			Col:		integer. Which column to sort by? [1 = first column]
			Delim:		string. If tab, must be '\\t'
			Sort_style:	string. 'n' or '' ['n' if column is numeric, empty if not]
			Header: 	boolean. Does the file have a header?

		Assumptions:
			File is not gz-zipped (or compressed at all)
			File ends in '.'txt'
			File has a single lined header, or no header

		Returns: filepath of the sorted file
	"""
	if type(File) is not str or type(In_dir) is not str or type(Out_dir) is not str:
		raise TypeError("File, In_dir, and Out_dir need to be strings.")
	if type(Col) is not int or Col <= 0:
		raise ValueError("Col needs to be an integer > 0.")
	if len(In_dir) > 0:	
		if not (os.path.isdir(In_dir)):
			raise ValueError(In_dir+" not found.")
		if In_dir[-1] != "/":
			raise ValueError("In_dir needs to end with a forward slash.")
	if len(Out_dir) > 0:	
		if not (os.path.isdir(Out_dir)):
			raise ValueError(Out_dir+" not found.")
		if Out_dir[-1] != "/":
			raise ValueError("Out_dir needs to end with a forward slash.")
	if File[-4:] != ".txt":
		raise ValueError("Please only use this function on .txt files.")
	if not os.path.isfile(In_dir+File):
		raise ValueError(File+" not found in directory\n"+In_dir)
	if type(Sort_style) is not str:
		raise TypeError("Sort_style needs to be a string")
	if Sort_style != "n" and Sort_style != "":
		raise ValueError("Sort_style needs to be 'n' or '', not: "+Sort_style)

	print "Passed bash_sort checks."

	in_file_path = In_dir + File	
	out_file_path = Out_dir + File[:-4]+"_sorted.txt"
	
	# Which column will be sorted by
	sort_at = str(Col)+","+str(Col)
	if Header:
		# Save the header to out_file
		command = "head " + in_file_path + " -n 1 > " + out_file_path
		call([command], shell= True)
				
		# This command is for checking if the column is already sorted.
		check_if_sorted_command = "tail -n +2 " + in_file_path + " | sort -t "+Delim+" -"+Sort_style+"k " + sort_at + " -c"
		test_sorted = call([check_if_sorted_command], shell = True)
		# If not sorted:
		if test_sorted == 1:
			# This sorts the file, but skips the header when sorting it, and writes the result to file
			command = "tail -n +2 " + in_file_path + " | sort -t "+Delim+" -"+Sort_style+"k " + sort_at + " >> " + out_file_path
			call([command], shell = True)
		# Else not sorted, just return original file path
		else:
			# Delete out_file that was going to be sorted
			command = "rm "+out_file_path
			call([command], shell = True)
			return in_file_path
	# Else no header
	else:
		# This command is for checking if the column is already sorted.
		check_if_sorted_command = "sort "+in_file_path+" -t "+Delim+" -"+Sort_style+"k " + sort_at + " -c"
		test_sorted = call([check_if_sorted_command], shell = True)
		# If not sorted:
		if test_sorted == 1:
		
			
			command = "sort "+in_file_path+" -t "+Delim+" -"+Sort_style+"k " + sort_at + " > " + out_file_path
			call([command], shell = True)
		# Else file is already sorted
		else:
			return in_file_path

	return out_file_path

try:
	if sort_style == "s":
		sort_style = ""
	# Check if delim is tab, fix it if it is
	if delim == "\t":
		fixed_delim = "\\t"
	else:
		fixed_delim = delim
	in_FILE = bash_sort(File = in_FILE, 
				In_dir = "",
				Out_dir = "",
				Col = Column_index+1,
				Delim = fixed_delim,
				Sort_style = sort_style,
				Header = True)
except BaseException:
	raise StandardError("bash_sort failed.")

all_row_groups = list()
row_group = "INITIATED"

f_IN = open(in_FILE, 'rb')
line_i = 0
for line in f_IN:
	if delim not in line:
		raise ValueError("Delim: "+delim+" doesn't seem to be the delim for the input file...")
	# Remove newline chars and split by tab
	split_line = line.rstrip('\r\n').split(delim)
	# If first line
	if line_i < 1:
		# If you want to keep all columns:
		if cols_to_keep == "all":
			# Get number of columns in first line of file
			n_cols = len(split_line)
			# make keep_col a list of all column indeces
			cols_to_keep = range(n_cols)
		
		# If there is a header:	
		if head == 1:
			# For each # in keep_col list, add the corresponding column from split_line to head
			head = [split_line[col_i] for col_i in cols_to_keep]
			line_i = line_i + 1
			continue
		
		line_i = line_i + 1

	if split_line[Column_index] == "":
		raise ValueError("Row value was empty at line: "+str(line_i)+". That's not cool.")

	if row_group == "INITIATED":
		# Initialize row_group list
		row_group_list = list()
		
		# Extract the value of the first row in the col of interest
		row_group = split_line[Column_index]
		# Add row_group to list
		row_group_list.append(row_group)
		# Add which line we're at to the list
		row_group_list.append(line_i)

		# Start saving data to row_group_file list
		row_group_file = list()
		if head == 1:
			row_group_file.append(head)
		kept_cols = [split_line[col_i] for col_i in cols_to_keep]
		row_group_file.append(kept_cols)

	# If this line's row_group is the same as the last, add it to the row_group file list
	elif split_line[Column_index] == row_group:
		kept_cols = [split_line[col_i] for col_i in cols_to_keep]
		row_group_file.append(kept_cols)

	# Check if current line of file's row_group is different from the last line checked
	elif split_line[Column_index] != row_group:
		# Add which line was last added (now we have the first and last lines)
		row_group_list.append(line_i-1)
		all_row_groups.append(row_group_list)

		# Write the contents of the row_group file list to a csv in its own directory
		filename = out_DIR+row_group+"/"+row_group+".BED.csv"
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		with open(filename, "wb") as f:
			writer = csv.writer(f)
			writer.writerows(row_group_file)

		# Re-initialize summary list
		row_group_list = list()
		# Add the first row_group row to the row_group list
		row_group = split_line[Column_index]
		row_group_list.append(row_group)
		row_group_list.append(line_i)

		# Re-initialize file list
		row_group_file = list()
		row_group_file.append(head)
		kept_cols = [split_line[col_i] for col_i in cols_to_keep]
		row_group_file.append(kept_cols)

	line_i = line_i + 1
f_IN.close()

for row_group in all_row_groups:
	print row_group[0]+": "+str(row_group[2]-row_group[1]+1)+" element(s)."
print "Completed folderize_by_column.py"
