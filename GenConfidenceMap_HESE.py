#this program calculates the -2llr distribution when set Ecut at the sliding energy
#output to shelve that contains norm, gamma, Ecut and the -rllr distribution
#later to be read and set confidence level
#need to do this for EHE, HESE, PEPE plus all three combined in the end

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
import shelve

if __name__ == "__main__":
    theReader = reader.input_HESE_shelve

    logLDistributions = {}
    EnergyBin = []
    count = 0
    iTotal = len(theReader)
    
    for iParam, iData in theReader.items(): #will run over 20 energy bins
        print "Processing ({}/{})...".format(count, iTotal), iParam
        if iData["cutoff"]!= myConfig.par_cutoff or iData["gamma"]!= myConfig.par_gamma:
            count += 1
            continue
        EnergyBin.append (iData["cutoff"])
        for _ in xrange(myConfig.nIter_confidence):
            pdf2d = iData["pdf_xy"]
            PseudoSet = PseudoExperiment.gen_pseudo(pdf2d)

            #the H0 is a loop over of all other possible Ecut
            H0_LLR = PseudoExperiment.get_H0_LLR(PseudoSet, theReader)

            #events, logL = asimov.get_dataset(pdf2d)

            Max_LLH = PseudoExperiment.get_Max_LLH(H0_LLR)
            #print _, logL
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(-2*(H0_LLR-Max_LLH))

        store = np.transpose(logLDistributions[iParam]) #[20,1000]
        gamma = iData["gamma"]
        norm = iData["norm"]
        cutoff = EnergyBin
        print EnergyBin
        eventstring = "para"
        
        quantile_90 = np.percentile(store[count][:],90)
        std = np.std(store[count][:])
            
        outputshelve = shelve.open(myConfig.output_HESE_shelve)
        outputshelve.clear()
        shelvewriter.write_shelve(outputshelve = outputshelve, index = eventstring, gamma = gamma, norm = norm, cutoff = cutoff, LLH = store )

    
        fig = plt.figure()
        ax = fig.gca()
        ax.hist(store[count][:], bins = 20)
        ax.set_title(r"CL_LLHratio_$\log\mathcal{{L}}={:.1f}\pm{:.1f}$" "\n" r"$(\gamma={:.2f},\mathrm{{norm}}={:.2E},\mathrm{{cutoff}}={:.2E})$"\
                     .format(quantile_90, std, iData["gamma"], iData["norm"], iData["cutoff"]))
        fig.savefig(os.path.join(myConfig.plotDirectory,"CL_LLHR_HESE_" + str(iParam) +"_"+ str(count) + ".png"))

        #print events
        print "...done"
        break

