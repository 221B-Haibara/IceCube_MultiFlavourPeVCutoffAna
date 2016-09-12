import numpy as np
from scipy.stats import poisson


def get_dataset(pdf2d):
    """
    Generate pseudo dataset from pdf2d
       pdf2d - array(energy, cosZenith) returning poisson probability
    """
    logL = 0
    events = []
    for iE, iCosZ, iMu in pdf2d:
        nEvents = np.random.poisson(iMu)
        for i in xrange(nEvents):
            events.append({"E":iE, "cosZenith":iCosZ, "weight":1})
        logL += poisson.pmf(nEvents, iMu)

    return events, logL
