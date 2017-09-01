# DLOG-tools

Workflow
========

1) Convert all .dlog tests to .csv
   - Use ./dlogToBareCsvCustom.sh for one file

   - Use ./serial_DlogToBareCsv.py to walk in a folder converting
     files

   Both use the dlogToCsv.m to work. Be sure to have GNU/Octave working

2)


Description
===========

* dlogToCsv.sh
    - This script converts a default KeySight dlog file to a KeySight csv
    - (The heavy-lifting of the number conversion is done by dlogToCsv.m using GNU/Octave)
    - Output: out.csv and out_bare.csv
    - Usage: ./dlogToCsv.sh filename.dlog output.csv
