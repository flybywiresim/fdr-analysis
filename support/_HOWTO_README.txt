FDR Fiels in WORK Folder 
========================

Microsoft Store Version
The work folder can be found here:
%LOCALAPPDATA%\Packages\Microsoft.FlightSimulator_8wekyb3d8bbwe\LocalState\packages\flybywire-aircraft-a320-neo\work\

Steam Version
The work folder can be found here:
%APPDATA%\Microsoft Flight Simulator\Packages\flybywire-aircraft-a320-neo\work\

FDR files are basically log files of a lot of parameters of the sim and the aircraft (ap/athr/fbw) in a special compressed format.

Every time the users starts a new flight a new file is created. For very long flight files are split into several files. 

Example file name: 2021-11-15-12-57-13.fdr

Create AP Report
================

Test FDR file: Test1.fdr

1. Convert the fdr file to csv

	fdr2csv_v11.exe -i .\Test1.fdr -o .\Test1.csv 
	
	(you might need to use v10 for Stable/Dev)

2. Get graph:

	fdr_analysis_ap.exe -f .\Test1.csv	


See example.png for explanation of the graphs. 
