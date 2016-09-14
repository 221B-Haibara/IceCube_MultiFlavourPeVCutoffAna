import sys
import argparse
from generator import PseudoExperiment, asimov
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

            PseudoSet = PseudoExperiment.gen_pseudo(pdf2d)
            Max_LLH = PseudoExperiment.get_Max_LLH(PseudoSet, pdf2d)
            print Max_LLH
            #the H0 is a loop over of all other possible Ecut
            H0_LLR = PseudoExperiment.get_H0_LLR(PseudoSet, Max_LLH, theReader)
            print H0_LLR

            #events, logL = asimov.get_dataset(pdf2d)
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(H0_LLR)
            #print _, logL
        
        for iE in xrange(len(theReader)):
            mean = np.mean(logLDistributions[iParam][iE])
            std = np.std(logLDistributions[iParam][iE])
            fig = plt.figure()
            ax = fig.gca()
            ax.hist(logLDistributions[iParam][iE])
            ax.set_title(r"LLHratio_$\log\mathcal{{L}}={:.1f}\pm{:.1f}$" "\n" r"$(\gamma={:.2f},\mathrm{{norm}}={:.2E},\mathrm{{cutoff}}={:.2E})$"\
                         .format(mean, std, iData["gamma"], iData["norm"], iData["cutoff"]))
            fig.savefig(os.path.join(myConfig.plotDirectory,"LLHR_" + str(iParam) +"_"+ str(iE) + ".png"))

        #print events
        print "...done"
        i += 1
        break
