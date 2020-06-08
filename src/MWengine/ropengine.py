#!/usr/bin/python

try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    print("[!] Cannot import the capstone module")
    sys.exit(1)

USEFUL_INSTRUCTIONS_OPERATIONS = (ARM_INS_MOV,ARM_INS_LDR,ARM_INS_STR)

class PreviousInstructionsSet:
    def __init__(self,i0,i1,i2,i3):
        self.i0=i0
        self.i1=i1
        self.i2=i2
        self.i3=i3

    def anyUseful(self):
        if(self.i0.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i1.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i2.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i3.id in USEFUL_INSTRUCTIONS_OPERATIONS):
            print("useful gadget")

class ARMRopSubengine:
    def __init__(self, dissas):

        self.dissas = dissas
        self.candidates = dict() #empty dictionary <instruction, PreviousInstructionsSet>
        print("[>] Rop Subengine Initialized")
    
    #find all POPs that pop the PC
    def locateReturns(self):
        for i in self.dissas:

            self.prevInst0=self.prevInst1
            self.prevInst1=self.prevInst2
            self.prevInst2=self.prevInst3
            self.prevInst3=i

            if i.id in (ARM_INS_POP) and len(i.operands) > 0:
                self.candidates[i] = PreviousInstructionsSet(self.prevInst0,self.prevInst1,self.prevInst2,self.prevInst3)


        