import numpy as np
from scipy.special import gamma

def get_dataset(pdf2d):
    """
    Generate pseudo dataset from pdf2d
       pdf2d - array(energy, cosZenith) returning poisson probability
    """
    logL = 0
    events = []
    for iE,iData in enumerate(pdf2d):
        for iCosZ, iMu in enumerate(iData):
            if iMu > 0: #FIXME and maybe gamma function
                logL += np.log(gamma(iMu))

    return list(), logL
