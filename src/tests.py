from capstone import *
from capstone.arm import *
import os
#CODE = b"\x09\x80\xBD\xE8"

filesize = os.path.getsize(str("D:\Github\MemWizard\src\ARMbigendianSample.bin"))
with open("D:\Github\MemWizard\src\ARMbigendianSample.bin", "rb") as f:
    memory = f.read(filesize)

CODE = memory

md = Cs(CS_ARCH_ARM,CS_MODE_ARM)

dis = md.disasm(CODE,0)

print("tipo: "+str(type(dis)))
for i in dis:
    print("pc" in i.op_str)
    print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
