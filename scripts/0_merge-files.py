#!/usr/bin/env python3

"""
Build a corpus for gensim from individual text files.
"""

# == imports ==

import os
import glob
from os.path import join
import re


# == parameters == 

workingdir = join("/", "media", "christof", "mydata", "Dropbox", "0-Analysen", "2018", "wfilm", "Nov18", "")
txtfolders = [join(workingdir, "data", "txt", "wfilm", "*11.txt")]
corpusfile = join(workingdir, "data", "txt", "wfilm11.txt")

seglen = 2000

# == functions == 


def get_basename(file): 
    basename = os.path.basename(file)
    return basename


def get_label(basename): 
    label = basename[0:2]
    return label
    

def get_text(file):
    with open(file, "r", encoding="utf8") as infile: 
        text = infile.read()#.lower()
        return text


def clean_text(text): 
    text = re.sub("[|]", " ", text) # encoding garbage
    text = re.sub("[\n|\t|«|»|¡|—| ]", " ", text) # special punctuation
    #text = re.sub("[,|;|?|!|\.|:|-|]", " ", text) # normal punctuation
    #text = re.sub("\d", "", text) # numbers
    text = re.sub("^ ", "", text)
    text = re.sub(" {1,100}", " ", text)
    text = [token for token in re.split(" ", text)]
    #text = " ".join(text)
    return text


def get_length(text): 
    length = len(text)
    return length


def build_line(basename, label, text, length, seglen): 
    numseg = length // seglen 
    #print(length, numseg)
    line = []
    if length > seglen: 
        for i in range(0,numseg): 
            start = (i*seglen)
            end = (i*seglen)+seglen
            segment = str(basename) + " " + " ".join(text[start:end])
            line.append(segment)
    return line


def save_corpus(lines, corpusfile): 
    with open(corpusfile, "w", encoding="utf8") as outfile: 
        outfile.writelines("%s\n" % line for line in lines)
                

# == main == 

def main(txtfolders, corpusfile, seglen):
    lines = []
    for folder in txtfolders:
        for file in glob.glob(folder): 
            basename,ext = get_basename(file).split(".")
            print(basename)
            label = get_label(basename)
            text = get_text(file)
            text = clean_text(text)
            length = get_length(text)
            line = build_line(basename, label, text, length, seglen)
            if line: 
                lines.extend(line)
    save_corpus(lines, corpusfile)
    
main(txtfolders, corpusfile, seglen)
