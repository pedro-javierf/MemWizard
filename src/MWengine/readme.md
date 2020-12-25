# MWengine 
The MWengine (short for Memory Wizard engine) is the submodule in charge of dissasembly and rop/jop finding tasks. It is divided in several submodules, most importantly:

 * MWengine.py which handles the dissasembly step, using the *capstone* library.
 * ROP and JOP engines, which receive the dissasembly and search for gadgets in it.
 
 **DISCLAIMER**: Current ROP and JOP engines are just test engines that perform a basic linear search looking for sample gadgets. This was used to test the GUI mostly.
