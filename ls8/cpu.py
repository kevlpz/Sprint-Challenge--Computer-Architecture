"""CPU functionality."""

import sys

ldi = 0b10000010
prn = 0b01000111
hlt = 0b00000001
mul = 0b10100010
add = 0b10100000
push = 0b01000101
pop = 0b01000110
call = 0b01010000
ret = 0b00010001
cmp = 0b10100111
jmp = 0b01010100
jeq = 0b01010101
jne = 0b01010110

gt = 0b10
lt = 0b100
et = 0b1

sp = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0b00000000
        self.running = True
        self.branch_table = {
            ldi: self.handle_ldi,
            prn: self.handle_prn,
            hlt: self.handle_hlt,
            mul: self.handle_mul,
            add: self.handle_add,
            push: self.handle_push,
            pop: self.handle_pop,
            call: self.handle_call,
            ret: self.handle_ret,
            cmp: self.handle_cmp,
            jmp: self.handle_jmp,
            jeq: self.handle_jeq,
            jne: self.handle_jne
        }
        self.flag = None

    def push(self, value):
        self.reg[sp] -= 1
        self.ram_write(value, self.reg[sp])

    def pop(self):
        value = self.ram_read(self.reg[sp])
        self.reg[sp] += 1
        return value

    def handle_ldi(self, operand_a, operand_b):
        print('ldi')
        self.reg[operand_a] = operand_b
        self.pc += 3
        
    def handle_prn(self, operand_a, operand_b):
        print('prn')
        print(self.reg[operand_a])
        self.pc += 2

    def handle_hlt(self, operand_a, operand_b):
        print('hlt')
        self.running = False

    def handle_mul(self, operand_a, operand_b):
        print('mul')
        self.alu('mul', operand_a, operand_b)
        self.pc += 3

    def handle_add(self, operand_a, operand_b):
        print('add')
        self.alu('add', operand_a, operand_b)
        self.pc += 3

    def handle_push(self, operand_a, operand_b):
        print('push')
        self.push(self.reg[operand_a])
        self.pc += 2

    def handle_pop(self, operand_a, operand_b):
        print('pop')
        self.reg[operand_a] = self.pop()
        self.pc += 2

    def handle_call(self, operand_a, operand_b):
        print('call')
        self.reg[sp] -= 1
        self.ram[self.reg[sp]] = self.pc + 2
        self.ram_write(self.reg[sp], self.pc + 2)

    def handle_ret(self, operand_a, operand_b):
        print('ret')
        self.pc = self.ram_read(self.reg[sp])
        self.reg[sp] += 1

    def handle_cmp(self, operand_a, operand_b):
        print('cmp')
        self.alu('cmp', operand_a, operand_b)
        self.pc += 3

    def handle_jmp(self, operand_a, operand_b):
        print('jmp')
        self.pc = self.reg[operand_a]

    def handle_jeq(self, operand_a, operand_b):
        print('jeq')
        if self.flag & et:
            self.pc = self.reg[operand_a] + 2
            # self.handle_jmp(self.reg[operand_a], None)
        else:
            self.pc += 2

    def handle_jne(self, operand_a, operand_b):
        print('jne')
        if not self.flag & et:
            print(f'jne operand_a: {operand_a}')
            print(f'jne reg[2]: {self.reg[2]}')
            self.pc = self.reg[operand_a] - 1
            # self.handle_jmp(self.reg[operand_a], None)
            print(f'jne pc: {self.pc}')
        else:
            self.pc += 2
            print('jne else')


    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar): # MAR = Memory Address Register, aka address
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr # MDR = Memory Data Register, aka value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "add":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "mul":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "cmp":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = lt

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = gt

            else:
                self.flag = et
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
        print('running...')
        while self.running:
            print(f'pc: {self.pc}')
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            print(f'self.ir: {bin(self.ir)}')
            if self.ir in self.branch_table:
                # print(f'self.ir: {self.ir}')
                # print(self.branch_table[self.ir])
                self.branch_table[self.ir](operand_a, operand_b)
            else:
                print('error')
                self.running = False
