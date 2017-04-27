import numpy as np
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--par_energybin', default=6, type=int) # 2481628.92284
parser.add_argument('--par_gammabin', default=7, type=int) # 2.31
#parser.add_argument('outfile')
opts = parser.parse_args()


class myConfig:
    nIter = 5000
    nIter_confidence = 1000
    outFileName = "logLDistributions.csv"
    makePlots = True
    plotDirectory = "./plots"

#loop gamma case
    gammabins = 30
    par_gammabin = opts.par_gammabin
    energybins = 20
    par_energybin = opts.par_energybin

    testbins_gamma=np.arange(1.59, 2.79, 0.04)

    testbins=np.logspace(6, 7.5, 20)

    par_gamma = testbins_gamma[par_gammabin]
    #par_cutoff = testbins[par_energybin]
    par_cutoff = 2481628.92284
    outputshelve = "Confidence_gamma_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"
    output_PEPE_shelve = "Confidence_gamma_PEPE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    
    output_HESE_shelve = "Confidence_gamma_HESE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    
    output_EHE_shelve = "Confidence_gamma_EHE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    

#loop energy case
"""
    par_gamma = 2.31
    energybins = 20
    par_energybin = opts.par_energybin
    testbins=np.logspace(6, 7.5, 20)
    par_cutoff = testbins[par_energybin]
    outputshelve = "Confidence_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"
    output_PEPE_shelve = "Confidence_PEPE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    
    output_HESE_shelve = "Confidence_HESE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    
    output_EHE_shelve = "Confidence_EHE_"+str(par_gamma)+"_"+str(par_cutoff)+".shelve"    

"""    
