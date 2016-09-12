import sys
import argparse
from generator import MCresample
import reader
from config import myConfig
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    theReader = reader.inputshelve
    logLDistributions = {}

    i = 0
    iTotal = len(theReader)
    for iParam, iData in theReader.items():
        print "Processing ({}/{})...".format(i, iTotal), iParam
        for _ in xrange(myConfig.nIter):
            pdf2d = iData["pdf_xy"]
            events, logL = MCresample.get_dataset(pdf2d)
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(logL)
            #print _, logL

        plt.figure()
        plt.hist(logLDistributions[iParam])
        plt.savefig(os.path.join(myConfig.plotDirectory,str(iParam) + ".png"))

        #print events
        print "...done"
        i += 1
