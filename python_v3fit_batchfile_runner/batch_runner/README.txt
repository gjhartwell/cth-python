The is the README file for the batch_runner folder

Greg Hartwell - July 24, 2020

Files and Usages

ReconServer User Manual - written by Mark Cianciosa - details how the recon server works

Folders:

    
    ReadV3Data      - files for reading the batch_runner 
                    - v3data and v3fit input files
    
    ReconStrings    - files that create strings and send them to the reconserver
        
    cthmds	    - wrapper routines for MDSPlus - gets CTH data from MDSPlus data base
    



Files:
    PythonBatchRunner   
                    - this is the main code
                    - provides a local GUI for running the batch runner.
                    - 

    chooseBatchFile     
                    - helper program for PythonBatchRunner
                    - lets user choose the batch file to runner
                    
    noBatchFileGivenErrorDialog
                    - dialog to display error when no batch file is given
                    - before trying to run batch_runner
                    
    readBatchFile   - defines the BathContents class and routines to 
		    - read, parse, and store information in the batch file



                    