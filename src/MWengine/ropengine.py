#!/usr/bin/python

try:
    from capstone import *
    from capstone.arm import *
except ImportError:
    print("[!] Cannot import the capstone module")
    sys.exit(1)

USEFUL_INSTRUCTIONS_OPERATIONS = [ARM_INS_MOV,ARM_INS_LDR,ARM_INS_STR]
KNOWN_RETURN_INSTRUCTIONS = [ARM_INS_POP]
PREVIOUS_THRESHOLD = 2

class PreviousInstructionsSet:
    def __init__(self,i0,i1,i2,i3):
        self.i0=i0
        self.i1=i1
        self.i2=i2
        self.i3=i3

    def isUseful(self):
        if(self.i0 != 0 and self.i1 != 0 and self.i2 != 0 and self.i3 !=0):
            if(self.i0.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i1.id in USEFUL_INSTRUCTIONS_OPERATIONS or self.i2.id in USEFUL_INSTRUCTIONS_OPERATIONS):
                return True

    def getFullGadgetData(self):
        '''self.i0.mnemonic + self.i0.op_str + "\n" +'''
        result =  self.i1.mnemonic + " " + self.i1.op_str + "\n" + self.i2.mnemonic + " " + self.i2.op_str + "\n" + self.i3.mnemonic + " " + self.i3.op_str
        return result

class ARMRopSubengine:
    def __init__(self, dissas):
        print(str(type(dissas)))
        self.dissas = dissas

        self.prevInst0=0
        self.prevInst1=0
        self.prevInst2=0
        self.prevInst3=0

        self.candidates = dict() #empty dictionary <instruction, PreviousInstructionsSet>
        
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
            
            '''
            print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
            if (i.id in KNOWN_RETURN_INSTRUCTIONS) and ("pc" in i.op_str):
                print("new gadget added")
                self.data[0].append(str(hex(i.address)))
                self.data[1].append(str(i.mnemonic) + str(i.op_str))
                self.data[2].append("ARM") '''
            
            self.prevInst0=self.prevInst1
            self.prevInst1=self.prevInst2
            self.prevInst2=self.prevInst3
            self.prevInst3=i
            
            if (i.id in KNOWN_RETURN_INSTRUCTIONS) and ("pc" in i.op_str):
                print("[*] possible gadget")
                self.candidates[i] = PreviousInstructionsSet(self.prevInst0,self.prevInst1,self.prevInst2,i)            

    def updateDataWithUseful(self):
        for key in self.candidates:
            if self.candidates[key].isUseful():
                print("[>] new gadget added")
                previousInstData = self.candidates[key].getFullGadgetData()
                self.data[0].append(str(hex(key.address)))
                self.data[1].append(previousInstData) #str(key.mnemonic) + str(key.op_str))
                self.data[2].append("ARM")


        