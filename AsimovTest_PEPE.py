#first generate median number of events from 'fake nature' of Lars best fit with cutoff
#then calculate the deltaLLH distribution vs cutoff energy for HESE, EHE, PEPE
## 3D loop over gamma, norm and cutoff
## project in 2D (gamma vs cutoff)
## for now assume same cutoff for nue and numu
## probability vs cutoff

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
    #H0_Reader = reader.input_HESE_shelve_3d #reader.H0_shelve
    H0_Reader = reader.input_HESE_shelve_3d #reader.H0_shelve
    
    logLDistributions = {}
    EnergyBin = []
    i = 0
    
    iTotal = len(H0_Reader)
    count = 0
#    for iParam, iData in H0_Reader.items():
#        EnergyBin.append (iData["cutoff"])
    for iParam, iData in H0_Reader.items(): #only use one set of specified data to generate data
        print "Processing ({}/{})...".format(count, iTotal), iParam
        if (iData["cutoff"]!= myConfig.par_cutoff or iData["gamma"]!= myConfig.par_gamma or iData["norm"]!= myConfig.par_norm):
            count += 1
            continue
        print "this is the Asimov set meow -------------------------------------------starting"
        for _ in xrange(myConfig.nIter):
            pdf2d = iData["pdf_xy"]

            H0_LLR = PseudoExperiment.get_H0_LLR(pdf2d, H0_Reader)

            Max_LLH = PseudoExperiment.get_Max_LLH(H0_LLR)

            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(-2*(H0_LLR-Max_LLH))

        #store = np.transpose(logLDistributions[iParam]) #[20,1000]
        store = logLDistributions[iParam]
        gamma = iData["gamma"]
        norm = iData["norm"]
        cutoff = iData["cutoff"]
        
        eventstring = "para"
        outputshelve = writer.output_PEPE_shelve
        #what it does is to generate -2LLR distributions when prior is set at H1 and scan over H0
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
            fig.savefig(os.path.join(myConfig.plotDirectory,"LLHR_PEPE_" + str(iParam) +"_"+ str(iE) + ".png"))

        #print events
        print "...done"
        i += 1
        break

