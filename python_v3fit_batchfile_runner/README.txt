python_v3fit_batchfile_runner
Greg Hartwell - August 13, 2020

This package runs V3FIT plasma/magnetic field equilibriums reconstructions in the python environment.
It is specific to data taken with on the Compact Toroidal Hybrid (CTH) expeiment at Auburn University.
The package mimics the functionality of the LabVIEW batch runner program written by Mark Cianciosa.

The progam reads a batch.cthsl shot list input file (see example file).
This in turn loads a v3data file to specity how the data is loaded and a v3config file
to set up the reconstruction.
Shots and times are then loaded.

The program reads and parses these files then creates reconstruction byte strings to pass to a remote server.
Then, the program waits for output files to be returned from the server and stores these files in the
appropriate directory. 







                    