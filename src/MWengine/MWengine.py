#!/usr/bin/python
import os
from MWengine.ropengine import ARMRopSubengine
try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    print("[!] Cannot import the capstone module")
    sys.exit(1)

AVAILABLE_ENGINES = ['ARM','ARM64']


#Dissasembly is done in this class and passed to the different engines to find rop gadgets
'''https://www.blopig.com/blog/2016/08/processing-large-files-using-python/'''
class MemWizardEngine:
    def __init__(self,architect='ARM'):
        # Set capstone values
        if(architect is 'ARM'):
            self.ropengine = ARMRopSubengine(0)
            self.jopengine = self.ropengine
            self.md = Cs(CS_ARCH_ARM, CS_MODE_ARM + CS_MODE_LITTLE_ENDIAN)
        else:
            self.ropengine = ARMRopSubengine(0)
            self.jopengine = self.ropengine
            self.md = Cs(CS_ARCH_ARM, CS_MODE_ARM + CS_MODE_LITTLE_ENDIAN)

        self.md.detail = True
        self.md.skipdata = True

        print("MemoryWizard engine started.")
    
    #Returns the information for the view tables
    def getROPData(self):
        return self.ropengine.getData()

    def getJOPData(self):
        return self.jopengine.getData()

    #1 load file in memory
    def loadFile(self, filename):
        #creates a dissasembled version of a binary in memory
        print(filename)
        try:
            filesize = os.path.getsize(str(filename[0])) #add huge memory checks
            with open(filename[0], "rb") as f:
                self.memory = f.read(filesize)

            self.dissasembly = self.md.disasm(self.memory,0)
            self.ropengine = ARMRopSubengine(self.dissasembly)
            self.loaded = True
        except:
            self.loaded = False
        return self.loaded
        
            

    #3 call analyzer engines
    def runAnalysis(self):
        if(self.loaded):
            self.ropengine.locateReturns()

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

    def searchROPGadget(self):
        print("[>] Starting ROP search task...")
        dissasemble()
        #self.ropengine = RopSubengine(self.binary, self.md.disasm(CODE, 0x0))
        self.ropengine.locateReturns()
        

    def searchJOPGadget(self):
        #search some jop gadget
        print("jop")

    