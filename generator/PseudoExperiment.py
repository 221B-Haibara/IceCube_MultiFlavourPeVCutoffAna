import numpy as np
from scipy.stats import poisson



def gen_pseudo(pdf2d): #effectively H1 case
    """
    Generate pseudo dataset from pdf2d
       return psedo dataset
    """
    PseudoSet = []
    for iE,iData in enumerate(pdf2d):
    
        for iCosZ, iMu in enumerate(iData):
    
            nEvents = np.random.poisson(iMu)
            PseudoSet.append([nEvents])
    #reshape from (350, 3) to (35, 10, 3)
    PseudoSet = np.reshape(PseudoSet,(35,10))
    return PseudoSet



def get_Max_LLH(PseudoSet, pdf2d): #effectively H1 case
    """
    Generate pseudo dataset from pdf2d
       pdf2d - array(energy, cosZenith) returning poisson probability
    """
    logL = 0
        
    for iE,iData in enumerate(PseudoSet):
        #print iE, iData
        for iCosZ, nEvents in enumerate(iData):
            #print iE,", ", iCosZ,", ", nEvents
            iMu = pdf2d[iE][iCosZ]

            if iMu > 0:
                logL += np.log(poisson.pmf(nEvents, iMu))

    return logL


def get_H0_LLR(PseudoSet, Max_LLH, theReader):
    """
    Calculate LLH ratio for a given set of psedo dataset generated at H1
       for pdf2d of H0- array(energy, cosZenith) [loopping over theReader]
    """
    pdf2d = []
    
    #loop over Ecut
    for jParam, jData in theReader.items():
        pdf2d.append( jData["pdf_xy"])
        
        #print jParam
    logL = np.zeros((len(theReader),))


    for iE,iData in enumerate(PseudoSet):
        for iCosZ, iMu in enumerate(iData):
            nEvents = iMu
            for kE in xrange(len(theReader)):
                exp = pdf2d[kE][iE][iCosZ]
                #print kE, iE, iCosZ, exp, iMu
                if exp >0:
                    logL[kE] += np.log(poisson.pmf(nEvents,exp ))
            
    return -2*(logL-Max_LLH)
