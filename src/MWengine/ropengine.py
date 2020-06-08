#!/usr/bin/python

try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    print("[!] Cannot import the capstone module")
    sys.exit(1)

class RopSubengine:
    def __init__(self, dissas):

        self.dissas = dissas
        self.retInstructionList=[] #empty list that will contain the found return instructions
        print("[>] Rop Subengine Initialized")
    
    def locateReturns(self):
        popList = []
        #find all POPs that pop the PC
        for i in self.dissas:
            if i.id in (ARM_INS_POP) and len(i.operands) > 0:
                popList.append(i)

        