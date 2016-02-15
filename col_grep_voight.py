#!/usr/bin/python

### col_grep.py
### Caleb Matthew Radens
### 2015_2_14

###    This script copies lines from a file that are grep-match-groupable at a column of interest,
###        and writes to file each matched group of lines to their own file, named after the group.
###
###    Arguments:
###        in_FILE
###            non-zipped
###        delim: how is the input file delimited? 
###            for comma, write: ,
###            for tab, write: tab
###        skip: How many lines to skip?
###            integer >= 0
###        Column_index: which column to group by
###            integer (0 is first column)
###        out_DIR: where should files by written to?
###            Extant directory
###
###    Assumptions:
###        The skipped lines aren't formatted like the rest of the file, and/or the col of interest
###            in the skipped lines are not grep-identical to any row below the skipped lines in
###            the col of interest.
###        ***The col of interest doesn't have something unix/bash-interpretable in it***
###
###    Usage:
###        python grep_col.py in_file.txt delim skip Column_# out_DIR

import sys, os
from subprocess import Popen
import time

print "Initiating folderize_by_column.py"
print "Argument List:", str(sys.argv[1:])

if (len(sys.argv)-1 != 5):
    raise Exception("Expected 5 command arguments.")
in_FILE = str(sys.argv[1])
delim = str(sys.argv[2])
skip = int(sys.argv[3])
Column_index = int(sys.argv[4])
out_DIR = str(sys.argv[5])

#pdb.set_trace()

if not (os.path.isfile(in_FILE)):
    raise ValueError(in_FILE+" not found. Is it a *full* and valid file path?")

# If tab-delimited, need to make sure it will be python-interpretable:
if delim != "," and delim != "tab":
    raise ValueError("delim needs to be ',' or 'tab', not '"+delim+"'")
    
if skip < 0:
    raise ValueError("Skip needs to be integer >= 0")

if Column_index < 0:
    raise ValueError("Skip needs to be integer >= 0")

if not (os.path.isdir(out_DIR)):
    raise ValueError(out_DIR+" not found. Is it a valid + extant directory?")

# Sub-python routine
if os.path.isfile("cowabunga.py"):
    print "FYI, we're overwriting something called 'cowabunga.py'"
with open("cowabunga.py", 'wb') as handle:
    handle.write("#!/usr/bin/python\n")
    handle.write("import sys, os, pdb\nfrom subprocess import call\n")
    handle.write("in_FILE = str(sys.argv[1])\n")
    handle.write("files = str(sys.argv[2])\n")
    handle.write("out_DIR = str(sys.argv[3])\n")
    handle.write("delim = str(sys.argv[4])\n")
    handle.write("if delim == 'tab':\n\tdelim='\t'\n")
    handle.write("Column_index = int(sys.argv[5])\n")
    handle.write("files = files.split(',')\n")
    handle.write("col_seps = Column_index * (\".*\"+delim)\n")
    handle.write("for f in files:\n")
    handle.write("\tout_FILE = os.path.join(out_DIR, f)\n")
    handle.write("\tout = call([\"grep $'\"+col_seps+\"\"+f+\"' \"+in_FILE+\" > \"+out_FILE],shell=True)")
    
# Convert delim to '\t' if it is tab
if delim == "tab":
    delim_check = '\t'
# Else delim is kept the same ',' in this case
else:
    delim_check = delim

# Get unique set of elements from column of interest
# Yes, I could combine the step after this into this loop, too,
#     but it's my house and I can do what I want.
groups = set()
i = 0
with open(in_FILE, 'rb') as handle:
    for line in handle:
        # Don't get unique elements from skipped lines
        if i < skip:
            i+=1
            continue
        if delim_check not in line:
            raise ValueError("You fool! '"+delim_check+"' isn't the delim of the file!")
        # Otherwise, get those unique elements from the col of interest
        if len(line.rstrip('\r\n').split(delim_check)[Column_index]) > 0: 
            groups.add(line.rstrip('\r\n').split(delim_check)[Column_index])
        else:
            raise ValueError("Line "+str(i)+" was empty in col of interest.")
        i+=1
lines_not_skipped = i-skip

# Want to grep 10 groups at a time from the file.
ten = list()
n_groups = len(groups)
i = 0
for group in groups:
    ten.insert(0,group) 
    i+=1
    # At every 10th group added to the list (or if end of groups reached):
    if len(ten) == 10 or i == n_groups:
        # Join each element with a comma
        joined=",".join(ten)
        # Generate the sys command
        command = in_FILE+" "+joined+" "+out_DIR+" "+delim+" "+str(Column_index)
        # Submit a system command, without waiting. Save error files just in case.
        proc = Popen(["bsub -e cowabunga.err -o cowabunga.out -q voight_normal python cowabunga.py "+command],shell=True,
            stdin=None, stdout=None, stderr=None, close_fds=True)
        if i != n_groups:
            ten = list()
        continue

# Wait for all groups to be written to file
group_check = list(groups)
while len(group_check) > 0:
    for f in os.listdir(out_DIR):
        if f in group_check and os.stat(os.path.join(out_DIR,f)).st_size > 0:
            group_check.remove(f)
    # Give the program a break: these are files my cowabunga minion script
    #  are trying to write to.
    time.sleep(5)

print "=============="
print "Processed "+str(lines_not_skipped)+" lines into "+str(len(groups))+" groups from file:\n"+in_FILE
print "Groups were written to directory:\n"+out_DIR
print "=============="
print "cowabunga.err looks like:"
with open("cowabunga.err") as handle:
    for line in handle:
        print line.rstrip("\n\r")
print "=============="
print "cowabunga.out looks like:"
with open("cowabunga.out") as handle:
    for line in handle:
        print line.rstrip("\n\r")
        
# Remove sub-routine and the error / out files
os.remove("cowabunga.py")
os.remove("cowabunga.err")
os.remove("cowabunga.out")
