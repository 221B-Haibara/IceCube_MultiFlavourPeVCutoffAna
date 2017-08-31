import numpy as np
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--par_energybin', default=13, type=int) # 2.21221629e+06 
parser.add_argument('--par_gammabin', default=14, type=int) # 2.31
parser.add_argument('--par_normbin', default=10, type=int) # 2.67
#parser.add_argument('--par_energybin', default=5, type=int) # 2481628.92284
#parser.add_argument('outfile')
#default aachen was 5, 14, 10 for the short version
opts = parser.parse_args()


class myConfig:
    nIter = 1
    nIter_confidence = 1000
    outFileName = "logLDistributions.csv"
    makePlots = True
    plotDirectory = "./plots"

    testbins_gamma=np.arange(1.59, 2.9, 0.05)
    #testbins=np.logspace(6, 7.5, 20)
    testbins=np.logspace(5, 8, 30)
    testbins_norm=np.arange(0.2, 4, 0.25)
    
    par_gammabin = opts.par_gammabin
    par_energybin = opts.par_energybin
    par_normbin = opts.par_normbin
    energybins = 30
    gammabins = 27
    normbins = 16
    par_gamma = testbins_gamma[par_gammabin]
    par_cutoff = testbins[par_energybin]   
    par_norm = testbins_norm[par_normbin]   
    #par_cutoff = 2481628.92284

    bin_edges_energy = {"track":[ 4.,4.2,4.4,4.6,4.8,5.,5.2,5.4,5.6,5.8,6.,6.2,6.4,6.6,6.8,7.,7.2,7.4,7.6], "cascade":[ 4.,4.2,4.4,4.6,4.8,5.,5.2,5.4,5.6,5.8,6.,6.2,6.4,6.6,6.8,7.,7.2,7.4,7.6]} # x
    bin_edges_zenith = {"track":[ -1.00000000e+00,-8.00000000e-01,-6.00000000e-01,-4.00000000e-01,-2.00000000e-01,-2.22044605e-16,2.00000000e-01,4.00000000e-01,6.00000000e-01,8.00000000e-01,1.00000000e+00], "cascade":[ -1, 0, 1]} # cos(z), y-coord


    
    outputshelve = "Confidence_gamma_"+str(par_gamma)+"_"+str(par_cutoff)+str(par_norm)+".shelve"
    output_PEPE_shelve = "Confidence_gamma_PEPE_"+str(par_gamma)+"_"+str(par_cutoff)+str(par_norm)+".shelve"    
    output_HESE_shelve = "Confidence_gamma_HESE_"+str(par_gamma)+"_"+str(par_cutoff)+str(par_norm)+".shelve"    
    output_EHE_shelve = "Confidence_gamma_EHE_"+str(par_gamma)+"_"+str(par_cutoff)+str(par_norm)+".shelve"    

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
