#!/usr/bin/python

import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import peakutils
import sys


def powerAverages_10tti(filename, expected_pks, szofinput, debug):
    period = 2.048E-5 #s
    measure_time = 3.0E-3 #s
    md = 9.5E-3/period
    slc_beg = 0
    slc_end = 300000

    inf_pt_thr = 0.7
    sup_pt_thr = 1.3
    events_per_sec = 1.0

    a,b = np.loadtxt(filename, delimiter=',', usecols=(0,1), unpack=True, dtype=float)

    if debug:
        A = [a[slc_beg:slc_end], b[slc_beg:slc_end]]
    else:
        A = [a,b]

    if debug:
        plt.plot(A[0], A[1], "g")
        plt.show()

    ind_peak_a = peakutils.indexes(A[1], thres=0.6, min_dist=md)

    l_ipa = len(ind_peak_a)

    ### CUT SECTION
    if (l_ipa > 1.3*expected_pks or l_ipa < 0.700*expected_pks) and not debug:
        print "This entry seems to have an error: " + str(l_ipa) + " points"
        plt.plot(A[0], A[1], "g")
        plt.show()
        beg = float(raw_input("startpoint: "))
        end = float(raw_input(" end point: "))

        beg *= len(A[0])/szofinput
        end *= len(A[0])/szofinput

        beg = int(math.floor(beg))
        end = int(math.floor(end))

        A[0] = A[0][beg:end]
        A[1] = A[1][beg:end]

        ind_peak_a = peakutils.indexes(A[1], thres=0.6, min_dist=md)

    ### ENDOFCUTTING

    pk_v_a = [ A[1][x] for x in ind_peak_a]
    pk_t_a = [ A[0][x] for x in ind_peak_a]

    if debug:
        plt.plot(A[0], A[1], "g", pk_t_a, pk_v_a, "*r")
        plt.show()

    #define parameters for measure
    half_sec = int(math.floor(0.5*(1.0E-3/period)))+1 #half chunk size
    #half_meas_dur  = int(math.floor((measure_time/period)/2)) + 1 #Tempo de medicao

    #print "half_sec ", half_sec, "half_meas_dur ", half_meas_dur

    mean_ttix_a = [[],[],[],[],[],[],[],[],[],[]]

    for peak in ind_peak_a:
        try:
            if peak > (12*half_sec) and (peak + 12*half_sec) < len(A[1]):
                for i in range(10):
                    mean_ttix_a[i].append(np.mean( A[1][ (peak+(-2-(5-i)*2)*half_sec):(peak+((-(5-i)*2))*half_sec)] ))
        except IndexError:
            pass

    mmean_ttix = [[],[],[],[],[],[],[],[],[],[]]

    for i in range(10):
        mmean_ttix[i] = np.mean(mean_ttix_a[i])*4*1000 #Multiply by voltage*1000 => mW

    try:
        varnum = int(filename.split('__')[1])
    except:
        varnum = "NO_VAR"

    try:
        filename = filename.split('/')[-1]
    except:
        pass

    print "\n" + filename

    print "NumPeaks : ", len(ind_peak_a)
    for i in range(10):
        print "Mean tti[", i, "] = ", mmean_ttix[i]

    v = [filename, varnum, str(len(ind_peak_a))]
    for i in range(10):
        v.append(mmean_ttix[i])

    return v

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage:", sys.argv[0],
        print "inputfile.csv outputfile.csv #expected_peaks duration(s)"
        print ""
        print "\t- If you have no idea how many peaks are expected, use 1"
        print ""
    else:
        filename = sys.argv[1]
        output = sys.argv[2]
        expected_pks = int(sys.argv[3])
        szofinput = int(sys.argv[4])
        target_dir = sys.argv[1]

        debug = False
        if len(sys.argv) == 6:
            if sys.argv[5] == "DEBUG":
                debug = True

        v = powerAverages_10tti(filename, expected_pks, szofinput, debug)
        with open(output, 'w') as o:
            for _ in v:
                print >>o,  str(v),
            print >>o, ""
