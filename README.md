# Report
Report in: https://albamrt.github.io/NMDA_fMRI_behavior/

# Instructions of usage:
1. Download this repository.
2. Create a folder named 'data' in the downloaded repository and place the data files 'NMDAEventsProjecteAj-EEGbeh.csv' and * and 'behaviour.csv'** in the folder.
3. Run the 'main.Rmd' file.
4. If wanted, upload the results back to GitHub.


\* The file 'NMDAEventsProjecteAj-EEGbeh.csv' can be obtained from REDCap by downloading the export name 'EEG_beh' (that includes the variables 'record_id', 'n_visit', 'testing', 'birthdate', 'gender', 'treatment', 'gaf_v0' and 'gaf'). If needed, rename the exported file to 'NMDAEventsProjecteAj-EEGbeh.csv'.

\** The file 'behaviour.csv' can be created by using the script 'concat_behavior.py' on the cluster. It concatenates the behavior files located in '/archive/albamrt/MRI/behaviour' and saves the concatenated file in '/storage/albamrt/NMDA/MRI/'.
