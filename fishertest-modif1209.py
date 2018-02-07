#!/usr/bin/python

import sys, argparse
import os
#from scipy.stats import chisquare
#from scipy.stats import fisher_exact
#from Fisher import fisher_exact
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

# ARGUMENTS
ARGS = {}             # Global dictionary

def parseoptions( ):
    """ Docstring 
    .... """
    #print " ".join( sys.argv )
    parser = argparse.ArgumentParser( description="" )
    parser.add_argument( '-i',  '--infile', default="M-GO_MF.tab2",  help="tableau de contingence")
    parser.add_argument( '-t',  '--threshold', default="0.05",  help="p value threshold, default 0.05")
    parser.add_argument( '-r',  '--res', default="T",  help="T,Tv or F. T (default) shows result of Chi2; Tv shows result of Chi2 plus difference with expected count by col; F shows line where Chi2 is not applicable")

    global ARGS        # Update the global ARGS variable 
    ARGS = parser.parse_args()

def getAllGO():
    with open(ARGS.infile,"r") as ef:
        for line in ef:
	   lS=line.split("\t")
    	   break

    allGO=[0]*(len(lS)-2)
    with open(ARGS.infile,"r") as ef:
        for line in ef:
             line=line.replace("\n","")
             lS=line.split("\t")
	     c=2
	     ca=0
	     while c < len(lS):		
		allGO[ca] = allGO[ca]+ int(lS[c])
   		c=c+1
		ca=ca+1
    tot_allGO=0
    for i in allGO:
	tot_allGO=i+ tot_allGO
    return tot_allGO, allGO

def getAllGO1():
    temp=(ARGS.lstnb)
    temp2=temp.split(",")
    allGO=[]
    tot_allGO=0
    for i in temp2:
        allGO.append(int(i))
        tot_allGO=tot_allGO + int(i)
    return tot_allGO, allGO

def getThisGO(lS):
             obs_thisGO=[]
             counter=2
             tot_thisGO=0
             while counter < len(lS):
                obs_thisGO.append(int(lS[counter]))
                tot_thisGO=tot_thisGO+int(lS[counter])
                counter=counter +1
	     return obs_thisGO, tot_thisGO 

def getObs_GOsp(obs_allGO, obs_thisGO):
    obs_GOsp=[]
    c=0
    while c < len(obs_allGO):
	m=obs_allGO[c] + obs_thisGO[c]
	obs_GOsp.append(m)
	c=c+1
    return obs_GOsp
    

def getExpected(obs_GOsp, tot_thisGO, tot):
    exp_thisGO=[]
    c=0
    for i in obs_GOsp:
	m=float(i*tot_thisGO)/float(tot)
	exp_thisGO.append(m)

    return exp_thisGO




def main():
    parseoptions()  
    
    tot_allGO, obs_allGO = getAllGO()
    #print obs_allGO, tot_allGO
    stats =  importr('stats', robject_translations={'format_perc': '_format_perc'})
    with open(ARGS.infile,"r") as ef:
	for line in ef:
	     line=line.replace("\n","")
	     lS=line.split("\t")
	     obs_thisGO, tot_thisGO = getThisGO(lS)
	     # obs_thisGO = [ , , ,]   tot_thisGO =int 
	     #print obs_thisGO, tot_thisGO	    
	     #obs_GOsp = getObs_GOsp(obs_allGO, obs_thisGO) --------------TO MODIF IF REUSED----------------------
	     #tot      = tot_thisGO + tot_allGO --------------TO MODIF IF REUSED----------------------

	     obs_GOsp = obs_allGO	
	     tot      = tot_allGO
 	     #print obs_GOsp , tot
	     
	     exp_thisGO	= getExpected(obs_GOsp, tot_thisGO, tot)
	     #exp_allGO  = getExpected(obs_GOsp, tot_allGO, tot) ----------TO MODIF IF REUSED-----------------------
       
	     #print exp_thisGO, tot_thisGO
	     #print exp_allGO, tot_allGO
	     #print obs_GOsp, tot
	     #print obs_allGO

   
	     test = robjects.r['rbind'](robjects.IntVector(obs_thisGO),  robjects.IntVector(obs_allGO))
             #print test

	     #value= stats.fisher_test(test, simulate.p.value=T ,  workspace=2e5)
	     pvalue= stats.fisher_test(test,simulate_p_value="TRUE")
	     pvalue= pvalue[0][0]
	     #print 'p-value: {}'.format(pvalue[0][0])
             # simulate.p.value=T  
	     m= line + "\t"+ str(pvalue)
             if pvalue < float(ARGS.threshold) : 
	     	 #if p_value[1] < float(ARGS.threshold) : 
			if ARGS.res =="T" or ARGS.res =="Tv" : print m    # ------------------------RESULT --------------------
			c=0
			temp=""
			while c < len(obs_thisGO):
				temp=temp +","+str(int(obs_thisGO[c] - exp_thisGO[c]))
				c=c+1
			if ARGS.res == "Tv" :print temp, "'- : obs < exp, + obs > exp" # --------------------- UNCOMMENT THIS ONE --------------
			#print "obs_thisGO", obs_thisGO
         	        #print "exp_thisGO", exp_thisGO
	


main()
                         
