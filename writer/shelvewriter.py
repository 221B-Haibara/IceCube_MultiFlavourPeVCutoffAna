def write_shelve(outputshelve,index, gamma,norm,cutoff,LLH):
    data = {}
    #data["gamma"] = float(gamma)
    data["norm"] = float(norm)
    data["cutoff"]= cutoff
    data["gamma"]= gamma
    data["LLHR"]= LLH
    outputshelve[index] = data
    outputshelve.close()
