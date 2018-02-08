#!/usr/bin/python

import sys, argparse
import os
from collections import defaultdict
import calc_dists_to_top_of_GO_using_bfs


# ARGUMENTS
ARGS = {}             # Global dictionary

def parseoptions( ):
    """ Docstring 
    .... """
    #print " ".join( sys.argv )
    parser = argparse.ArgumentParser( description="" )
    parser.add_argument( '-l',  '--lst', default='MR-GO.tab1 MF-GO.tab1 ML-GO.tab1 ME-GO.tab1 MC-GO.tab1"',  help="lst  ")
     
    global ARGS        # Update the global ARGS variable 
    ARGS = parser.parse_args()
    

def main():
    parseoptions( )
    temp= ARGS.lst
    
    lst= temp.split(" ")
    c=-1
    dico={}
    dicoEcc={}
    dicoTyp={}
    for file in lst:
	c=c+1
	with open(file,"r") as ef:
	    for line in ef:
		line=line.replace("\n","")
		lS=line.split("\t")
		if lS[0] not in dico:
		      l=[0]*5
		      dico[lS[0]]=l
		      try :dicoTyp[lS[0]] = lS[2]
		      except: dicoTyp[lS[0]] = "unknown"
		      try: dicoEcc[lS[0]] = lS[3]
		      except: dicoEcc[lS[0]] = lS[0]	
		dico[lS[0]][c]=lS[1]
	
    print "type\tGO\tMR\tMF\tML\tME\tMC"	
    for i in dico:
	m= str(dicoTyp[i])+"\t"+str(dicoEcc[i]) 
	for j in dico[i]:
		m=m+"\t"+str(j)
	print m

main()
                         
