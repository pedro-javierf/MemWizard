#!/usr/bin/python

from MWview.MWview import MemWizardGUI

VERSION = "1.0"
DEBUG = True

def debug(text):
    if(DEBUG):
        print(str(text))

def main():
    debug("MemWizard v"+ VERSION)
    mainWindow = MemWizardGUI()

if __name__ == '__main__':
    main()