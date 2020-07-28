The is the README file for the batch_runner folder

Greg Hartwell - July 24, 2020

Files and Usages

ReconServer User Manual - written by Mark Cianciosa - details how the recon server works

Folders:
    Dialog Testing  - test files for python dialog gui
    
    olderUnusedFiles- files that I don't think are used anymore
                    - but I didn't want to delete
    
    ReadV3Data      - files for reading the batch_runner 
                    - v3data and v3fit input files
    
    tcp_client_and_server
        
                    - simple test tcp client and server examples
    TestReconFiles  - holds batch, v3data, and v3fit input files for testing
                    - is being used as a test folder as recon directories
                    - are created here
    



Files:
    PythonBatchRunner   
                    - this is the main code
                    - provides a local GUI for running the batch runner.
                    - 

    chooseBatchFile     
                    - helper program for PythonBatchRunner
                    - lets user choose the batch file to runner
                    
    makeReconDirs       
                    - creates directories for all shots listed
                    - in the batch file
                    
    noBatchFileGivenErrorDialog
                    - dialog to display error when no batch file is given
                    - before trying to run batch_runner
                    
    readBatchFile   - defines the BathContents class and routines to 
		    - read, parse, and store information in the batch file



                    