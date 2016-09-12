import numpy as np


def get_dataset(pdf2d):
    """
    Generate pseudo dataset from pdf2d
       pdf2d - array(energy, cosZenith) returning poisson probability
    """
    events = []
    for iE, iCosZ, iMy in pdf2d:
        events.append({"E":iE, "cosZenith":iCosZ, "weight":1})
    return events
