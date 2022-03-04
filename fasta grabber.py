# -*- coding: utf-8 -*-
"""
Created on Fri May 29 19:06:29 2020

@author: elizm
"""

import Bio
from Bio import Entrez

import time

Entrez.email = '' #enter email here

#enter search terms/results, get IDs, and file name for ID list

def gis_search(search):
    handle = Entrez.esearch(db = 'gene', term = search, retmax = 600, idtype ='acc')
    record = Entrez.read(handle)
    handle.close()
    gis = record.get("IdList")
    print("%s results, continue? \n" % len(gis))
    ans = input("y or n? \n")
    if ans == "y": 
        print("okay, going to the fasta grabber\n")
        file = input("file name: ")
        filename = file + ".txt"
        fasta_grabber(gis,filename)
    else:
        print("okay, goodbye")
        main()

#grab sequences using ID and format them to fasta

def fasta_grabber(gis,filename):
    acclist = []
    startlist = []
    stoplist = [] #lists to store the correct location of sequences
    print("obtaining Accession Numbers...")
    for gi in gis:
        try:
            handle = Entrez.esummary(db = 'nucleotide', id = gi, retmode="xml")
            records = Entrez.read(handle)
            acc = records["DocumentSummarySet"]['DocumentSummary'][0]["LocationHist"][0]['ChrAccVer']
            start = records["DocumentSummarySet"]['DocumentSummary'][0]["LocationHist"][0]['ChrStart']                                                         
            stop = records["DocumentSummarySet"]['DocumentSummary'][0]["LocationHist"][0]['ChrStop']
            start = int(start) + 1
            stop = int(stop) + 1
            acclist.append(acc)
            startlist.append(start)
            stoplist.append(stop)
   
        except:
            print("error with GID " + gi)


    with open(filename,'w+') as f:
        f.write("%s results" % len(acclist))
        
    print("%s results without error \n" % len(acclist))
    
    print("now grabbing Fasta sequences...")
    
    count = 0

# get the correct sequence in the correct location then convert to fasta txt

    for acc in acclist:
        acc = str(acc)    
        start = str(startlist[count])
        stop = str(stoplist[count])
        handle = Entrez.efetch(db="nucleotide", id=acc, rettype="fasta", retmode = "xml" ,  seq_start = start, seq_stop= stop)
        fetch = Entrez.read(handle)
        sequins = fetch[0]['TSeq_sequence']
        organism = fetch[0]['TSeq_defline']
        count = count + 1
        print( count, "sequences completed")
        fastaseq = ">" + acc + ":" + start + "-" + stop + " " + organism + "\n" + sequins
        with open(filename,'a+') as f:
            f.write("\n" + fastaseq + "\n") #output is file with filename "_ results.txt"

    print("action complete!")
    main()
    

def main():
    search = input("search: ")
    
    gis_search(search)
    
if __name__ == "__main__":
    main()
