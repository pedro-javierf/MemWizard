from capstone import *
from capstone.arm import *
CODE = b"\x09\x80\xBD\xE8"
md = Cs(CS_ARCH_ARM,CS_MODE_ARM)


for i in md.disasm(CODE,0):
    print("pc" in i.op_str)
    print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))
