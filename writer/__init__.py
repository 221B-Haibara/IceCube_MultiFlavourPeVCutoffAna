import shelve
#outputshelve = shelve.open("./outputShelve.shelve")
#output_Cascade_shelve = shelve.open("./output_Cascade_Shelve.shelve")
output_PEPE_shelve = shelve.open("./output_PEPE_Shelve_Asimov.shelve")
#output_HESE_shelve = shelve.open("./output_HESE_Shelve.shelve")
#output_EHE_shelve = shelve.open("./output_EHE_Shelve.shelve")
#output_gamma_PEPE_shelve = shelve.open("./output_gamma_PEPE_Shelve.shelve")
#output_gamma_HESE_shelve = shelve.open("./output_gamma_HESE_Shelve.shelve")
#output_gamma_EHE_shelve = shelve.open("./output_gamma_EHE_Shelve.shelve")
output_PEPE_shelve.clear()

def fresh_shelve(name):   
    output_shelve = shelve.open("./output_{}_Shelve.shelve".format(name))
    output_shelve.clear()
    return output_shelve
