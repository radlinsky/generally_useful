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
###      head: how many lines of stuff before the data begins?
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
###  Usage:
###    python split_at_column.py in_file file_delim head out_file col_i col_delim replace

import sys
import os
import csv
from subprocess import call

print "Initiating split_at_column.py"
print "Argument List:", str(sys.argv[1:])

if (len(sys.argv)-1 != 7):
    raise Exception("Expected seven command arguments.")

in_FILE = str(sys.argv[1])
file_delim = str(sys.argv[2])
head = int(sys.argv[3])
out_file = str(sys.argv[4])
col_i = int(sys.argv[5])
col_delim = str(sys.argv[6])
replace = str(sys.argv[7])

if not (os.path.isfile(in_FILE)):
    raise ValueError(in_FILE+" not found. Is it a *full* and valid file path?")
if not head >= 0:
    raise ValueError("head should be integer >= 0")
if not os.path.isdir(os.path.dirname(out_file)):
    raise ValueError(out_file+" can't be written because the parent dir doesn't exist.")
if col_i < 0:
    raise Exception("col_i needs to be an integer >= 0.")
if replace != "y" or replace != "n":
    raise ValueError("replace needs to be 'y' or 'n' [lowercase]")