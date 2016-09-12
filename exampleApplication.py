import sys
import argparse
from generator import MCresample
import reader
from config import myConfig
import matplotlib.pyplot as plt

if __name__ == "__main__":
    theReader = reader.shelvereader
    logLDistributions = {}

    for iParam in theReader:
        for _ in xrange(myConfig.nIter):
            pdf2d = theReader.get_pdf_from_file(f)
            events, logL = MCresample.get_dataset(pdf2d)
            if not logLDistributions.has_key(iParam):
                logLDistributions[iParam] = []
            logLDistributions[iParam].append(logL)

        plt.hist(logLDistributions[iParam])
        plt.savefig(os.path.join(myConfig.plotDirectory,str(iParam) + ".png"))

    print "If everything worked, these are the generated events:"
    print events
