import numpy as np
from scipy.stats import poisson


def get_dataset(pdf2d):
    """
    Generate pseudo dataset from pdf2d
       pdf2d - array(energy, cosZenith) returning poisson probability
    """
    logL = 0
    events = []
    for iE,iData in enumerate(pdf2d):
        for iCosZ, iMu in enumerate(iData):
            nEvents = np.random.poisson(iMu)
            for i in xrange(nEvents):
                events.append({"E":iE, "cosZenith":iCosZ, "weight":1})
            if iMu > 0: #FIXME and maybe gamma function
                logL += poisson.pmf(nEvents, iMu)

    return events, logL
