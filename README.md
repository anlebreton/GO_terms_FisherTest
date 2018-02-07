# GO_terms_FisherTest
Initially created to find significant differences of GO categories occurrences among a set of species


INPUT EXAMPLE : species1_F1.tab

IDgene1 \t GO:0007050,GO:0008570

IDgene2 \t GO:0008270

summarizeGO4plot.py -i species1_F1.tab > species1_F2.tab

species1_F2.tab : GO term \t nbr_occurence_in_species1_F1.tab \t CC/MF/BP \t GO_description

GO:0030428 \t 3 \t cellular_component \t cell septum

GO:0008103 \t 1 \t biological_process \t oocyte microtubule cytoskeleton polarization

summarizeGO4plot-tab.py -l "species1_F2.tab species2_F2.tab species3_F2.tab [...]" > table_GO.tab

table_GO.tab : CC/MF/BP \t GO_description \t nbr_occurence_in_species1_F1.tab \t nbr_occurence_in_species2_F1.tab \t nbr_occurence_in_species3_F1.tab 

biological_process \t small molecule metabolic process \t 52 \t 25 \t 21 

biological_process \t establishment of organelle localization \t 1 \t 1 \t0

fisher_test.py -i table_GO.tab
