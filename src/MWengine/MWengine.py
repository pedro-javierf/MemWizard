#!/usr/bin/python

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
        filesize = os.path.getsize(filename)
        with open(filename, "rb") as f:
            memory = f.read(filesize)
    
    


'''https://www.blopig.com/blog/2016/08/processing-large-files-using-python/'''
class MemWizardEngine:
    def __init__(self):
        # Do something
        print("MemoryWizard engine started.")
    
    def loadFile(self, filename):
        #creates a dissasembled version of a binary in memory
        print("ni")

    def searchROPGadget(self):
        #search some rop gadgted
        print("ni")

    def searchJOPGadget(self):
        #search some jop gadget
        print("ni")

    