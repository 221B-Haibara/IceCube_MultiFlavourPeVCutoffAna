def write_shelve(outputshelve,index, gamma,norm,cutoff,LLH):
    data = {}
    data["gamma"] = float(gamma)
    data["norm"] = float(norm)
    data["cutoff"]= float(cutoff)
    data["LLHR"]= LLH
    outputshelve[index] = data
    outputshelve.close()
