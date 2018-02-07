#!/usr/bin/python

import sys, argparse
import os
from collections import defaultdict
import calc_dists_to_top_of_GO_using_bfs


# ARGUMENTS
ARGS = {}             # Global dictionary

def parseoptions( ):
    """ /!\ needs calc_dists_to_top_of_GO_using_bfs available at  https://gist.github.com/avrilcoghlan/8671799
    .... """
    #print " ".join( sys.argv )
    parser = argparse.ArgumentParser( description="" )
    parser.add_argument( '-i',  '--infile',default="MR-GO.tab",  help="[GO annotation, ID \t GO:1,GO:2 etc.]")
    parser.add_argument( '-obo',  '--obo',default="go-basic.obo",  help="[obo file]; I used the go-basic.obo file from http://geneontology.org/page/download-ontology ")
    parser.add_argument( '-l',  '--level', default="2",  help="level in GO hierachy starting from the top, BP,CC and MF are at level 0")
    parser.add_argument( '-btw',  '--btw', default="No",  help="Yes - get GO between root and chosen level, default No ")
    parser.add_argument( '-d',  '--description', default="term.txt",  help="None or file path; default term.txt (file with the correspondance between GO id and GO description")
  
    global ARGS        # Update the global ARGS variable 
    ARGS = parser.parse_args()

#INPUT EXAMPLE
#MC|c4600_g1_i1-m.9872   GO:0007050,GO:0008570
#MC|c7771_g1_i1-m.18561  GO:0008270
#MC|c527_g1_i2-m.11866   GO:0005783,GO:0006487,GO:0006488,GO:0031965,GO:0016740,GO:0030176,GO:0004577

def getGOToDisplay(parents):
    lstout=['GO:0003674','GO:0005575', 'GO:0008150']
    c=0
    lst2=lstout
    while c < int(ARGS.level):
      c=c+1
      lst    = lstout
      lstout = []

      for go in lst:
	for i in parents:
	     if  go in parents[i]:
		lstout.append(i)
      lst2=lst2+lstout   


	#print lstout
        #print c,ARGS.level	
    #print "FIN =============================================="
    if ARGS.btw != "No" : return lst2
    return lstout


def fillDico(line, dico, lstGO, parents):
    #c7231_g1_i1     GO:0008270
    #c4184_g1_i1     GO:0005634,GO:0097236,GO:0008270,GO:0006366,GO:0000981,GO:0000977
    
    line=line.replace("\n","")
    lS=line.split("\t")
    lS2=lS[1].split(",")
    lst2=[]
    for go in lS2:
	dicoAncestor= calc_dists_to_top_of_GO_using_bfs.BFS_dist_from_node(go, parents)
	lst= list(set(dicoAncestor.keys()).intersection(lstGO))
	#if "GO:0019748" in lst: print "####################### ", lS[0]
	#if len(lst) != 1 : print "warning 0 or more than 1 go detected", lst, go
	
	for i in lst:
	   if i not in lst2:
		lst2.append(i)

    for i in lst2:
        if i in dico:
	     dico[i]=dico[i] +1
	else: dico[i] = 1
    return dico	

def createDicoDesc():
    dico={}
    with open(ARGS.description,"r") as ef:
      for line in ef:
        if "GO:" in line :
            lS=line.split("\t")
	    m= str(lS[2]) +"\t"+ str(lS[1])

            dico[lS[3]]=m
    return dico

def main():
    parseoptions()     # Parse sys.argv if you want quick and dirty script
    # sys.argv[ 0 ] : name of the pgm
    (parents, terms) = calc_dists_to_top_of_GO_using_bfs.read_go_ancestors(ARGS.obo)

    lstGO=getGOToDisplay(parents)
    #for i in parents:
	#print i, parents[i]
    dico={}
    cc=0
    with open(ARGS.infile,"r") as ef:
      for line in ef:	
	dico = fillDico(line, dico, lstGO, parents)

    if ARGS.description != "None":
	dicoDesc=createDicoDesc()

	for i in dico:
	    try:
		print str(i)+"\t"+str(dico[i])+"\t"+str(dicoDesc[i])
	    except:
		print str(i)+"\t"+str(dico[i])

    else:
        for i in dico:
                print str(i)+"\t"+str(dico[i])


main()
                         
