#!/usr/bin/python
import os
try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    print("[!] Cannot import the capstone module")
    sys.exit(1)

class Binary:
    filesize=0
    memory=[]
    def __init__(self,filename):
        filesize = os.path.getsize(str(filename[0]))
        with open(filename[0], "rb") as f:
            memory = f.read(filesize)
    
    
'''https://www.blopig.com/blog/2016/08/processing-large-files-using-python/'''
class MemWizardEngine:
    def __init__(self):
        # Do something
        print("MemoryWizard engine started.")
    
    def loadFile(self, filename):
        #creates a dissasembled version of a binary in memory
        print(filename)
        self.binary = Binary(filename)
        self.loaded = True
        #return true
        
    def runAnalysis(self):
        if(self.loaded):
            md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
            md.detail = True


    def searchROPGadget(self):
        #search some rop gadgted
        print("ni")

    def searchJOPGadget(self):
        #search some jop gadget
        print("ni")

    