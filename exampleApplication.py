import sys
import argparse
from generator import MCresample, asimov
import reader
from config import myConfig
import matplotlib.pyplot as plt
import os
import numpy as np

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
            #events, logL = asimov.get_dataset(pdf2d)
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(logL)
            #print _, logL

        mean = np.mean(logLDistributions[iParam])
        std = np.std(logLDistributions[iParam])
        fig = plt.figure()
        ax = fig.gca()
        ax.hist(logLDistributions[iParam])
        ax.set_title(r"$\log\mathcal{{L}}={:.1f}\pm{:.1f}$" "\n" r"$(\gamma={:.2f},\mathrm{{norm}}={:.2E},\mathrm{{cutoff}}={:.2E})$"\
                     .format(mean, std, iData["gamma"], iData["norm"], iData["cutoff"]))
        fig.savefig(os.path.join(myConfig.plotDirectory,str(iParam) + ".png"))

        #print events
        print "...done"
        i += 1
