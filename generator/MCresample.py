import numpy as np


def get_dataset(2dpdf):
"""
Generate pseudo dataset from 2dpdf
 2dpdf - array(energy, cosZenith) returning poisson probability
"""
    events = []
    for iE, iCosZ, iMy in 2dpdf:
        nEvents = np.random.poisson(iMy)
        for i in xrange(nEvents):
            events.append({"E":iE, "cosZenith":iCosZ, "weight":1})
    return events
