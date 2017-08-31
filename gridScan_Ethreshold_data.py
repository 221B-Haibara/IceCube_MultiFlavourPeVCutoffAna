#first generate median number of events from 'fake nature' of Lars best fit with cutoff
#then calculate the deltaLLH distribution vs cutoff energy for HESE, EHE, PEPE
## 3D loop over gamma, norm and cutoff
## project in 2D (gamma vs cutoff)
## for now assume same cutoff for nue and numu
## probability vs cutoff
###this script now is hacked to find energy threshold to support high energy spectrum fit
###to test
### "LE:", testbins_gamma[25], testbins_norm[10], testbins[3]
### "HE:", testbins_gamma[12], testbins_norm[5], testbins[18]

import sys
import argparse
from generator import PseudoExperiment, asimov
import reader
from reader import txtfilereader
import writer
from writer import shelvewriter
from config import myConfig
import matplotlib.pyplot as plt
import os
import numpy as np

if __name__ == "__main__":
    #H0_Reader = reader.input_PEPE_shelve_3d #reader.H0_shelve
    #H0_Reader = reader.input_HESE_shelve_3d #reader.H0_shelve
    H0_Reader = reader.input_EHE_shelve_3d #reader.H0_shelve
    #H0_Reader = reader.input_PEPE_shelve_3d_05 #reader.H0_shelve
    txtfilereader.get_pdf_from_file("data/HESE_data.csv", myConfig)
    exit()
    
    satDistributions = {}
    logLDistributions = {}
    maxLLHDistributions = {}
    EnergyBin = []
    bestfit = {}

    iTotal = len(H0_Reader)
    count = 0
    pdf2d = None
    for iParam, iData in H0_Reader.items(): #only use one set of specified data to generate data
        print "Processing ({}/{})...".format(count, iTotal), iParam
        if (iData["cutoff"]== myConfig.testbins[3] and iData["gamma"]== myConfig.testbins_gamma[25] and iData["norm"]== myConfig.testbins_norm[10]) or \
           (iData["cutoff"]== myConfig.testbins[18] and iData["gamma"]== myConfig.testbins_gamma[12] and iData["norm"]== myConfig.testbins_norm[5]):
            count += 1
            
            if pdf2d == None:
                pdf2d = iData["pdf_xy"]
            else:
                pdf2d += iData["pdf_xy"]
        if count==2:
            break
### "LE:", testbins_gamma[25], testbins_norm[10], testbins[3]
### "HE:", testbins_gamma[12], testbins_norm[5], testbins[18]

        print "this is the Asimov set meow -------------------------------------------starting"

    for iEnergyThBin in xrange(0,18):

        H0_LLR = PseudoExperiment.get_H0_LLR(pdf2d, H0_Reader, iEnergyThBin)
        Max_LLH = PseudoExperiment.get_Max_LLH(H0_LLR, iEnergyThBin)
        Sat_LLR,ndf = PseudoExperiment.get_Sat_LLR(pdf2d, iEnergyThBin)
        para = PseudoExperiment.max_bin(pdf2d, H0_Reader,Max_LLH, iEnergyThBin)
        #ndf = ndf - 2. 
        #logLDistributions["combined"].append(-2*(H0_LLR-Max_LLH))
        #logLDistributions[iEnergyThBin] = (-2*(H0_LLR-Max_LLH))
        satDistributions[iEnergyThBin] = Sat_LLR/ndf
        maxLLHDistributions[iEnergyThBin] = Max_LLH/ndf
        logLDistributions[iEnergyThBin] = (-2*(Max_LLH-Sat_LLR))/ndf
        bestfit[iEnergyThBin] = para
        print "meow maximum likelihood is ", Max_LLH/ndf
        binwidth = 0.2
        maxlim = 7.5
        #lim = ( int(xymax/binwidth) + 1) * binwidth
        lim=4
        yetAnotherEnergyConversion = np.arange(lim, maxlim + binwidth, binwidth)

        print "bin =", iEnergyThBin, yetAnotherEnergyConversion[iEnergyThBin], ndf, logLDistributions[iEnergyThBin]
        continue

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

fig = plt.figure()
ax = fig.gca()
x = map(lambda x: yetAnotherEnergyConversion[x], logLDistributions.keys())
y = logLDistributions.values()
ax.plot(x,y)
fig.savefig(os.path.join(myConfig.plotDirectory,"energyThres.png"))
print y
print x

fig = plt.figure()
ax = fig.gca()
x = map(lambda x: yetAnotherEnergyConversion[x], maxLLHDistributions.keys())
y = maxLLHDistributions.values()
ax.plot(x,y)
fig.savefig(os.path.join(myConfig.plotDirectory,"energyThres_maxLLH.png"))

fig = plt.figure()
ax = fig.gca()
x = map(lambda x: yetAnotherEnergyConversion[x], satDistributions.keys())
y = satDistributions.values()
ax.plot(x,y)
fig.savefig(os.path.join(myConfig.plotDirectory,"energyThres_sat.png"))


fig = plt.figure()
ax = fig.gca()
x = map(lambda x: yetAnotherEnergyConversion[x], bestfit.keys())
y = bestfit.values()
print y
#ax.plot(x,y)
#fig.savefig(os.path.join(myConfig.plotDirectory,"energyThres_sat.png"))
