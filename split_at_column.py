#/usr/bin/python

# split_at_column.py
# Caleb Matthew Radens
# 2016_2_7

### This script splits a file at a user-defined column with a specified delim and
###     writes new file with the column split up.
###
###  Arguments:
###      in_file: non-zipped delimited file
###
###      file_delim: how is the file delimited?
###          String.
###
###      skip: how many lines of stuff to skip?
###          Integer.
###
###      out_file: what should the new file be named?
###          Cannot overwrite the original file.
###
###      col_i: Which col to split? (0 = 1st col)
###          Integer.
###
###      Col_delim: What character should split the col?
###
###      Replace: Keep the original column or discard it?
###          'y' or 'n'
###  
###      Assumptions:
###          Column of interest is identically formatted at every row.
###
###  Examples:
###    split_me_up | col2 | col3
###
###    replace = 'n'
###    split | me | up | split_me_up | col2 | col3
###
###    replace = 'y'
###    split | me | up | col2 | col3
###  Usage:
###    python split_at_column.py in_file file_delim skip out_file col_i col_delim replace

import sys
import os
import csv

print "Initiating split_at_column.py"
print "Argument List:", str(sys.argv[1:])

if (len(sys.argv)-1 != 7):
    raise Exception("Expected seven command arguments.")

in_FILE = str(sys.argv[1])
file_delim = str(sys.argv[2])
skip = int(sys.argv[3])
out_FILE = str(sys.argv[4])
col_i = int(sys.argv[5])
col_delim = str(sys.argv[6])
replace = str(sys.argv[7])

if not (os.path.isfile(in_FILE)):
    raise ValueError(in_FILE+" not found. Is it a *full* and valid file path?")
# from bash, >>> python \t sends a 't' to python. >>> python $'\t' sends \t.
#    this little check assumes user meant \t
if "t" in file_delim and len(file_delim)==1:
    file_delim = "\t"
if not skip >= 0:
    raise ValueError("skip should be integer >= 0")
if not os.path.isdir(os.path.dirname(out_FILE)):
    raise ValueError(out_FILE+" can't be written because the parent dir doesn't exist.")
if col_i < 0:
    raise Exception("col_i needs to be an integer >= 0.")
if replace != "y" and replace != "n":
    raise ValueError("replace needs to be 'y' or 'n' [lowercase]")

# Open output file
with open(out_FILE, 'wb') as csv_file_handle:
    writer = csv.writer(csv_file_handle)
    # Open input file
    with open(in_FILE, 'rb') as file_handle:
        i = 0
        # Skip lines until i >= skip
        for line in file_handle:
            if i < skip:
                continue
            if file_delim not in line:
                raise ValueError("Delim: '"+file_delim+"' doesn't seem to be the delim this line:\n"+line)
            split_line = line.rstrip('\r\n').split(file_delim)
            
            # Pop off column if replace = 'y'
            if replace == "y":
                col_to_split = split_line.pop(col_i)
            # Else keep the column
            else:
                col_to_split = split_line[col_i]
            if col_delim not in col_to_split:
                raise ValueError("Delim: '"+col_delim+"' doesn't seem to be in the col of interest at line "+str(i))
            
            # Split the column at specified delim
            split_col = col_to_split.split(col_delim)
            
            # Add the split column elements to the beginning of the row, preserving order of the split col
            while len(split_col) > 0:
                split_line.insert(0, split_col.pop())
            
            # Write row with column split up to the new file
            writer.writerow(split_line)
            i = i + 1










