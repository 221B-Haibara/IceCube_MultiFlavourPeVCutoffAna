import numpy as np
from scipy.stats import poisson, gamma as gammafunc



def gen_pseudo(pdf2d): #effectively H1 case
    """
    Generate pseudo dataset from pdf2d
       return psedo dataset
    """
    PseudoSet = []
    for iE,iData in enumerate(pdf2d):
        #print np.shape(pdf2d)
        for iCosZ, iMu in enumerate(iData):

            nEvents = np.random.poisson(iMu)
            PseudoSet.append([nEvents])
    #reshape from (350, 3) to (35, 10, 3)
    #PseudoSet = np.reshape(PseudoSet,(35,10)) #meow!! hardcoded number (35,20) for tracks
    PseudoSet = np.reshape(PseudoSet,np.shape(pdf2d)) #meow!! hardcoded number (35,20) for tracks
    
    return PseudoSet



def get_Max_LLH(H0_LLR,energyThresBin = 0): #effectively H1 case
    """
    To find out the maximum likelihood value by looping over H0_LLR and find out max    
    """
    logL = np.amax(H0_LLR)
    print "maximum likelihood is ", logL
    return logL

wrongNormHack = 3.13170779665e-17
wrongNormHack_data = 3.13170779665e-17*6./4.6

testbins_gamma=np.arange(1.59, 2.9, 0.05)
#testbins=np.logspace(6, 7.5, 20)
testbins=np.logspace(5., 8., 30)
testbins_norm=np.arange(0.2, 4, 0.25)
para_bin = []
for i in xrange(len(testbins_gamma)):
            for j in xrange(len(testbins_norm)):
                for k in xrange(len(testbins)):
                    Ecut = testbins[k]
                    gamma = testbins_gamma[i]
                    norm = testbins_norm[j]
                    para_bin.append([Ecut,gamma,norm])
                    

def get_H0_LLR(PseudoSet, theReader, energyThresBin = 0):
    """
x    Calculate LLH ratio for a given set of psedo dataset generated at H1
       for pdf2d of H0- array(energy, cosZenith) [loopping over theReader]
    """
    pdf2d = []
    
    #loop over Ecut
    for jParam in para_bin: 
        jData = theReader.get("{}_{}_{}".format(jParam[1],jParam[2],jParam[0]))
        pdf2d.append( jData["pdf_xy"])
        
        #print jParam
    logL = np.zeros((len(theReader),))


    for iE,iData in enumerate(PseudoSet):
        if iE < energyThresBin: #only use high energy
        #if iE >=7: #only use low energy
            continue
        for iCosZ, iMu in enumerate(iData):
            nEvents = iMu
            for kE in xrange(len(theReader)):
                expec = pdf2d[kE][iE][iCosZ]
                #print kE, iE, iCosZ, exp, iMu
                if expec >0.:
                    #print nEvents*wrongNormHack,expec*wrongNormHack, np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                    #logL[kE] += np.log(poisson.pmf(nEvents*wrongNormHack,expec*wrongNormHack))
                    #logL[kE] +=np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                     
                    #logL[kE] += ( expec*wrongNormHack- nEvents*wrongNormHack * np.log(expec*wrongNormHack));
                    logL[kE] += ( expec*wrongNormHack- nEvents*wrongNormHack_data * np.log(expec*wrongNormHack));
                    
    return logL*(-1.)


def max_bin(PseudoSet, theReader, maxLLH, energyThresBin = 0):
    """
    Calculate LLH ratio for a given set of psedo dataset generated at H1
       for pdf2d of H0- array(energy, cosZenith) [loopping over theReader]
    """
    pdf2d = []
    
    #loop over Ecut
    for jParam in para_bin: 
        jData = theReader.get("{}_{}_{}".format(jParam[1],jParam[2],jParam[0]))
        pdf2d.append( jData["pdf_xy"])
        
        #print jParam
    logL = np.zeros((len(theReader),))


    for iE,iData in enumerate(PseudoSet):
        if iE < energyThresBin: #only use high energy
        #if iE >=7: #only use low energy
            continue
        for iCosZ, iMu in enumerate(iData):
            nEvents = iMu
            for kE in xrange(len(theReader)):
                expec = pdf2d[kE][iE][iCosZ]
                #print kE, iE, iCosZ, exp, iMu
                if expec >0.:
                    #print nEvents*wrongNormHack,expec*wrongNormHack, np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                    #logL[kE] += np.log(poisson.pmf(nEvents*wrongNormHack,expec*wrongNormHack))
                    #logL[kE] +=np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                    #logL[kE] += ( expec*wrongNormHack- nEvents*wrongNormHack * np.log(expec*wrongNormHack));
                    logL[kE] += ( expec*wrongNormHack- nEvents*wrongNormHack_data * np.log(expec*wrongNormHack));
                if logL[kE]*-1. ==maxLLH:
                    print "*** best fit *** ", para_bin[kE], logL[kE]*-1
                    bestfitE = para_bin[kE]
    return bestfitE


def get_Sat_LLR(PseudoSet, energyThresBin = 0):
    """
    Calculate LLH ratio for a given set of psedo dataset generated at H1
       for pdf2d of H0- array(energy, cosZenith) [loopping over theReader]
    """

    logL = 0
    ndf=0
    for iE,iData in enumerate(PseudoSet):
        if iE < energyThresBin: #only use high energ
            continue
        for iCosZ, iMu in enumerate(iData):

            ndf+=1
            nEvents = iMu
            expec = PseudoSet[iE][iCosZ]
            print "debugging meow", iE, iCosZ, expec*wrongNormHack, nEvents*wrongNormHack_data
            #print kE, iE, iCosZ, exp, iMu
            if expec >0.:
                #print nEvents*wrongNormHack,expec*wrongNormHack, np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                #logL[kE] += np.log(poisson.pmf(nEvents*wrongNormHack,expec*wrongNormHack))
                #logL[kE] +=np.log(gammafunc.pdf(nEvents*wrongNormHack,expec*wrongNormHack))
                #logL += ( expec*wrongNormHack- nEvents*wrongNormHack * np.log(expec*wrongNormHack));
                logL += ( expec*wrongNormHack- nEvents*wrongNormHack_data * np.log(expec*wrongNormHack));
                    
    return logL*(-1.),ndf
