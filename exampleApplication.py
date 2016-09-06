import sys
import argparse
from generator import MCresample
from reader import txtfilereader

if __name__ == "__main__":
    with open("example.txt") as f:
        pdf2d = txtfilereader.get_pdf_from_file(f)
    events = MCresample.get_dataset(pdf2d)

    print "If everything worked, these are the generated events:"
    print events
