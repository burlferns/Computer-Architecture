"""CPU functionality."""
import sys

###########################
# Command opcodes
###########################
HLT = 0b00000001 # halt & exit --- HLT
LDI = 0b10000010 # load register immediate --- LDI register integer
MUL = 0b10100010 #
PRN = 0b01000111 # print register contents --- PRN register
##########################

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0 # program counter
        self.fl = 0 # flags register 00000LGE
        self.ir = 0 # instruction register
        self.running = True
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL

    def handle_HLT(self):
        self.running = False

    def handle_LDI(self):
        reg_addr = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg_addr] = value

    def handle_PRN(self):
        reg_addr = self.ram_read(self.pc+1)
        value = self.reg[reg_addr]
        print(value)

    def handle_MUL(self):
        regA_addr = self.ram_read(self.pc+1)
        regB_addr = self.ram_read(self.pc+2)
        self.alu("MUL",regA_addr,regB_addr)

    def load(self,program):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def ram_read(self,mar):
        return self.ram[mar]

    def ram_write(self,mar,mdr):
        self.ram[mar] = mdr


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            self.ir = self.ram_read(self.pc)

            if self.ir in self.branchtable:
                self.branchtable[self.ir]()
                inst_len = ((self.ir & 0b11000000) >> 6) + 1
                self.pc += inst_len
            else:
                print("Unknown instruction")
                self.running = False

            
