### reads the unbilded data and converts it into shelve like structure just like the MC shelves....
import numpy as np
import pandas as pd

def get_pdf_from_file(fname, cfg):
    df = pd.read_csv(fname)
    df.zenith = np.cos(np.deg2rad(df.zenith))
    df.energy = np.log10(df.energy)
    trackorcas = "cascade" if ("PEPE" in fname or "HESE" in fname) else "track"
    pdf_xy = np.histogram2d(df.energy, df.zenith, bins=[cfg.bin_edges_energy[trackorcas], cfg.bin_edges_zenith[trackorcas]])[0]
    return pdf_xy


        
