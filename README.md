# GO_terms_FisherTest
Initially created to find significant differences of GO categories occurrences among a set of species

input is a tabular file without header (yet), comparisons are made starting at the 3rd column to the end. 
I used it with first column corresponding to biological_process, molecular_function or cellular_component, second column with a description of GO term, other columns are the number of occurence of the corresponding GO term with each column corresponding to a species.

biological_process      cellular component maintenance  0       0       0       1       0
biological_process      platelet formation      0       0       1       0       0
biological_process      developmental pigmentation      0       0       1       4       0
biological_process      small molecule metabolic process        52      25      21      159     53
