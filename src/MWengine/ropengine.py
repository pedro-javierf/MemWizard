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

    def isUseful(self):
        if(self.i0.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i1.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i2.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i3.id in USEFUL_INSTRUCTIONS_OPERATIONS):
            return True

    def isUseless(self):
        return not isUseful(self)

class ARMRopSubengine:
    def __init__(self, dissas):
        print(str(type(dissas)))
        self.dissas = dissas
        #self.candidates = dict() #empty dictionary <instruction, PreviousInstructionsSet>
        self.data = dict()
        self.data[0] = [] #new empty list for addresses
        self.data[1] = [] #new empty list for gadget mnemonics
        self.data[2] = [] #new empty list for mode string
        print("[>] Rop Subengine Initialized")
    
    def getData(self):
        return self.data

    #find all POPs that pop the PC. i.e:
    #POP {R3,R0,PC}
    #LDMFD    sp!, {r3,r0,pc}
    def locateReturns(self):
        for i in self.dissas:
            
            print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
            if("pc" in i.op_str):
                print("new gadget added")
                self.data[0].append(str(hex(i.address)))
                self.data[1].append(str(i.mnemonic) + str(i.op_str))
                self.data[2].append("ARM") 
            '''
            self.prevInst0=self.prevInst1
            self.prevInst1=self.prevInst2
            self.prevInst2=self.prevInst3
            self.prevInst3=i
            
            if i.id in (ARM_INS_POP) and ("pc" in i.op_str):
                self.candidates[i] = PreviousInstructionsSet(self.prevInst0,self.prevInst1,self.prevInst2,self.prevInst3)'''               



        