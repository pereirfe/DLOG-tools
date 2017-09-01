#!/usr/bin/python

import os
import fnmatch
from subprocess import call
import sys

def serial_dlogToCsv(target_dir, output_dir, op_path):
    format_in = ".dlog"
    format_out = ".csv"


    for subdir, dirs, files in os.walk(target_dir, followlinks=True):
        for f in files:
            if f.endswith(format_in):
                tgtf = target_dir + f
                call([op_path, tgtf, (os.path.splitext(tgtf)[0]+format_out) ])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:", sys.argv[0],
        print "dlog_directory [csv_directory] [path_to_dlogToCsv.sh]"
        print ""
        print "\t- If csv_directory not informed, it will be equal to dlog_directory"
        print "\t- If path_to_dlogToCsv not informed, assumed local"
        print ""
    else:
        target_dir = sys.argv[1]
        output_dir = target_dir
        op_path = "./dlogToCsv.sh"

        if len(sys.argv) >= 3:
            output_dir = sys.argv[2]

        if len(sys.argv) >= 4:
            op_path = sys.argv[3]

        serial_dlogToCsv(target_dir, output_dir, op_path)
