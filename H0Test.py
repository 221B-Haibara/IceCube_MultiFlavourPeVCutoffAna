import sys
import argparse
from generator import PseudoExperiment, asimov
import reader
import writer
from writer import shelvewriter
from config import myConfig
import matplotlib.pyplot as plt
import os
import numpy as np

if __name__ == "__main__":
    H0_Reader = reader.H0_shelve
    theReader = reader.inputshelve

    logLDistributions = {}
    EnergyBin = []
    i = 0
    #iTotal = len(theReader)
    iTotal = len(H0_Reader)

    for iParam, iData in theReader.items():
        EnergyBin.append (iData["cutoff"])
    for iParam, iData in H0_Reader.items():
        print "Processing ({}/{})...".format(i, iTotal), iParam
        for _ in xrange(myConfig.nIter):
            pdf2d = iData["pdf_xy"]
            PseudoSet = PseudoExperiment.gen_pseudo(pdf2d)
            Max_LLH = PseudoExperiment.get_Max_LLH(PseudoSet, pdf2d)
            #print Max_LLH
            #the H0 is a loop over of all other possible Ecut
            H0_LLR = PseudoExperiment.get_H0_LLR(PseudoSet, Max_LLH, theReader)
            #print H0_LLR

            #events, logL = asimov.get_dataset(pdf2d)
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(H0_LLR)
            #print _, logL

        store = np.transpose(logLDistributions[iParam]) #[20,1000]
        gamma = iData["gamma"]
        norm = iData["norm"]
        cutoff = EnergyBin
        print EnergyBin
        eventstring = "para"
        outputshelve = writer.outputshelve
        shelvewriter.write_shelve(outputshelve = outputshelve, index = eventstring, gamma = gamma, norm = norm, cutoff = cutoff, LLH = store )
        #shelvewriter.write_shelve(outputshelve = "outputShelve.shelve", index = 1, 2.49,8,1000, LLH =store )

        for iE in xrange(len(store)):
            
            mean = np.mean(store[iE][:])
            std = np.std(store[iE][:])
            fig = plt.figure()
            ax = fig.gca()
            ax.hist(store[iE][:], bins = 20)
            ax.set_title(r"LLHratio_$\log\mathcal{{L}}={:.1f}\pm{:.1f}$" "\n" r"$(\gamma={:.2f},\mathrm{{norm}}={:.2E},\mathrm{{cutoff}}={:.2E})$"\
                         .format(mean, std, iData["gamma"], iData["norm"], iData["cutoff"]))
            fig.savefig(os.path.join(myConfig.plotDirectory,"LLHR_" + str(iParam) +"_"+ str(iE) + ".png"))

        #print events
        print "...done"
        i += 1
        break

