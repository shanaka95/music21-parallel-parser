## Description

Music21 is a widely used python based toolkit used in machine learning. When you need to deal with midi filies, you need to parse them first and generate a list of notes. When you have a large dataset, it takes a lot time to parse all the files. 

There is an prebuilt parallel runner inside music21 library. But it did not give me a good result. So I created this script to parallaly run a few threads and speed up parsing process 

## Usage

Change number of threads, midi files location,  and output file location in the script.

run script

`python3 parse.py`
