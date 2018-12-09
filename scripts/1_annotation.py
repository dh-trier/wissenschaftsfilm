#!/usr/bin/env python3

"""
Annotate text files with Freeling 4.1. 
"""

# == imports ==

import os
import glob
from os.path import join
import re
import subprocess
# requires Freeling!


# == parameters == 

workingdir = join("/", "media", "christof", "mydata", "Dropbox", "0-Analysen", "2018", "wfilm", "Nov18", "")
inputfile = join(workingdir, "data", "txt", "wfilm11.txt")
outputfile = join(workingdir, "data", "ann", "wfilm11.txt")


# == functions == 

def read_file(inputfile): 
    with open(inputfile, "r", encoding="utf8") as infile: 
        text = infile.read()
        return text


def annotate_text(inputfile, outputfile): 
    command = "/usr/local/bin/analyze -f en.cfg < " + inputfile
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    annotated = result.stdout.decode("utf-8").split("\n")
    return annotated


def filter_annotated(annotated): 
    filtered = []
    for item in annotated: 
        item = item.split(" ") # Freeling
        if len(item) == 4: 
            if item[0][0:3] in ["wf0", "wf1", "nf0", "nf1"]:
                print(item[0])
                filtered.append("\n" + item[0])
            #elif item[2] in ["NP", "NN"] and "_" not in item[1] and float(item[3]) > 0.6:  # Freeling
            elif item[2] in ["NP", "NN"] and "_" not in item[1]:  # Freeling
                print(item)
                filtered.append(item[0])
    return filtered
    

def save_annotated(filtered, outputfile): 
    with open(outputfile, "w", encoding="utf8") as outfile: 
        outfile.writelines("%s\n" % line for line in filtered)


def main(inputfile, outputfile):
    basename = os.path.basename(inputfile)
    annotated = annotate_text(inputfile, outputfile)
    filtered = filter_annotated(annotated)
    save_annotated(filtered, outputfile)
    
main(inputfile, outputfile)
