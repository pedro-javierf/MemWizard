#!/usr/bin/python

from MWview.MWview import MemWizardGUI
from MWengine.MWengine import MemWizardEngine

VERSION = "1.0"
DEBUG = True

def debug(text):
    if(DEBUG):
        print(str(text))

def main():
    debug("MemWizard v"+ VERSION)
    engine = MemWizardEngine()
    mainWindow = MemWizardGUI(engine)

if __name__ == '__main__':
    main()