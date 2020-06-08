#!/usr/bin/python
import os
from MWengine.ropengine import ARMRopSubengine
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
        # Set default capstone values
        self.md = Cs(CS_ARCH_ARM, CS_MODE_ARM + CS_MODE_LITTLE_ENDIAN)
        self.md.detail = True
        self.md.skipdata = True
        print("MemoryWizard engine started.")
    
    def loadFile(self, filename):
        #creates a dissasembled version of a binary in memory
        print(filename)
        self.binary = Binary(filename)
        self.loaded = True
        #return true
        
    def runAnalysis(self):
        if(self.loaded):
            self.md.detail = True

    #Dynamically change the architecture
    def changeArchitecture(self, newArch, endianess):
        if(endianess):
            e=CS_MODE_LITTLE_ENDIAN
        else:
            e=CS_MODE_BIG_ENDIAN

        if(newArch=="ARM"):
            self.md = Cs(CS_ARCH_ARM, CS_MODE_ARM + e)
        elif(newArch=="ARM_THUMB"):
            self.md = Cs(CS_ARCH_ARM, CS_MODE_THUMB + e)
        elif(newArch=="ARM64"):
            self.md = Cs(CS_ARCH_ARM64, CS_MODE_ARM) #no endianness?
        elif(newArch=="x86"):
            self.md = Cs(CS_ARCH_X86, CS_MODE_32 + e)
        elif(newArch=="x86-64"):
            self.md = Cs(CS_ARCH_X86, CS_MODE_64 + e)
        else:
            print("ERROR")

    def dissasemble(self):
        #choose the correct subengine depending on the architecture
        #if(archo==arm ARMRopSubengine)
        self.ropengine = ARMRopSubengine(self.binary, self.md.disasm(CODE, 0x0))

    def searchROPGadget(self):
        print("[>] Starting ROP search task...")
        dissasemble()
        #self.ropengine = RopSubengine(self.binary, self.md.disasm(CODE, 0x0))
        self.ropengine.locateReturns()
        

    def searchJOPGadget(self):
        #search some jop gadget
        print("jop")

    