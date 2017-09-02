#!/usr/bin/python

import os
import fnmatch
from subprocess import call
import sys
from powerAverages_10tti import powerAverages_10tti
from operator import itemgetter

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage:", sys.argv[0],
        print "csv_directory outputfile expected_peaks size_of_input"
        print ""
    else:
        target_dir = sys.argv[1]
        output_file = sys.argv[2]
        expected_pks = int(sys.argv[3])
        szofinput = int(sys.argv[4])

        if target_dir[-1] != '/':
            target_dir += '/'

        format_in = ".csv"

        res = []
        for subdir, dirs, files in os.walk(target_dir, followlinks=False):
            for f in files:
                if f.endswith(format_in):
                    tgtf = target_dir + f
                    v = powerAverages_10tti(tgtf, expected_pks, szofinput, False)
                    res.append(v)

        sorted_res = sorted(res, key=itemgetter(1))

        with open(output_file, 'w') as o:
            for line in sorted_res:
                for i, v in enumerate(line):
                    if i == len(line)-1:
                        print >>o, str(v)
                    else:
                        print >>o, str(v)+',',
