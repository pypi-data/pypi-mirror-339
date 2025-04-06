import colorama
import time
import socket
import zipfile
import io
import copy
import threading
import random
from io import BytesIO


colorama.init()
hardware_memory_addresses = [
    0xFFFF0000,
    0xFFFF0100,
    0xFFFF0101,
    0xFFFF0102,
    0xFFFF0103,
    0xFFFF0104,
    0xFFFF0105,
    0xFFFF0106,
    0xFFFF0107,
]


engine_lock_fs = threading.Lock()
"""Engine class"""
cdef class Engine:
    cdef int mode
    cdef list stack
    cdef dict code_addresses
    cdef int code_len
    cdef list ret_pcs
    cdef Hardware hardware
    cdef int pc
    cdef object zip
    cdef object debug
    cdef dict register
    cdef dict memory
    cdef dict flags
    cdef dict OPCODES
    cdef object stop_event
    cdef tuple code_memory
    """initializer"""
    def __init__(self, dict data_sector, dict code_sector, dict mem_sector, zip: BytesIO, debug:bool=False, ):
        self.mode = 0x12
        self.zip: BytesIO = zip
        self.stack = []
        self.hardware = Hardware(debug)
        self.debug = debug
        self.register = {i: 0 for i in range(0x10, 0x3C)}
        self.memory = {**mem_sector,**data_sector, **code_sector}


        sorted_items = sorted(code_sector.items())
        self.code_memory = tuple(value for key, value in sorted_items)
        self.code_addresses = {key: index for index, (key, value) in enumerate(sorted_items)}
        self.code_len = len(sorted_items)


        self.flags = {'ZF': 0, 'CF': 0, 'SF': 0, 'OF': 0}
        self.pc = 0
        self.ret_pcs = []
        self.OPCODES = {
            '1b': self.add, '1c': self.sub, '1d': self.mul, '1e': self.div,
            '1f': self.mod, '20': self.pow, '2a': self.and_op, '2b': self.or_op,
            '2c': self.xor, '2d': self.not_op, '2e': self.shl, '2f': self.shr,
            '40': self.load, '41': self.store, '42': self.cmp, '43': self.jmp,
            '44': self.je, '45': self.jne, '46': self.jg, '47': self.jl,
            '48': self.mov, '49': self.interrupt, '4a': self.change_mode,
            '4b': self.call, '4c': self.ret, '4d': self.push, '4e': self.pop,
            '4f': self.swap, '50': self.dup, '51': self.drop, '52': self.halt,
            '53': self.rand, '54': self.inc, '55': self.dec, '56': self.abs,
            '57': self.neg,
        }
        self.stop_event = threading.Event()
        for i in hardware_memory_addresses:
            self.memory[i] = None
    """Kill engine"""
    def kill(self):
        self.stop_event.set()
    """Run"""
    cpdef run(self):
        try:
            while self.pc < self.code_len and not self.stop_event.is_set():
                op = self.code_memory[self.pc]
                if self.debug:
                    print(f"[Execute] [Address:{hex(self.pc)}] {op}")
                self.execute(op)
                self.pc += 1
        except KeyError as e:
            print(f"[ERROR] Key Error: {e}")
            raise e
        except KeyboardInterrupt:
            return (self.zip)
        except StopEngineInterrupt:
            return (self.zip)
        return (self.zip)
    cdef void execute(self, op):
        opcode: str = op[0]
        if opcode in self.OPCODES:
            self.OPCODES[opcode](op) 
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    cdef void add(self, tuple op): self.register[op[1]] += self.register[op[2]]
    cdef void sub(self, tuple op): self.register[op[1]] -= self.register[op[2]]
    cdef void mul(self, tuple op): self.register[op[1]] *= self.register[op[2]]
    cdef void div(self, tuple op): self.register[op[1]] //= self.register[op[2]]
    cdef void mod(self, tuple op): self.register[op[1]] %= self.register[op[2]]
    cdef void pow(self, tuple op): self.register[op[1]] **= self.register[op[2]]

    cdef void and_op(self, tuple op): self.register[op[1]] &= self.register[op[2]]
    cdef void or_op(self, tuple op): self.register[op[1]] |= self.register[op[2]]
    cdef void xor(self, tuple op): self.register[op[1]] ^= self.register[op[2]]
    cdef void not_op(self, tuple op): self.register[op[1]] = ~self.register[op[1]]
    cdef void shl(self, tuple op): self.register[op[1]] <<= op[2]
    cdef void shr(self, tuple op): self.register[op[1]] >>= op[2]

    cdef void load(self, tuple op): self.register[op[1]] = self.memory[op[2]]
    cdef void store(self, tuple op): self.memory[op[2]] = self.register[op[1]]

    cdef void jmp(self, tuple op): self.jump(op[1])
    cdef void je(self, tuple op):  # Jump if equal
        if self.flags['ZF']: self.jump(op[1])
    cdef void jne(self, tuple op):  # Jump if not equal
        if not self.flags['ZF']: self.jump(op[1])
    cdef void jg(self, tuple op):  # Jump if greater
        if not self.flags['ZF'] and self.flags['SF'] == self.flags['OF']: self.jump(op[1])
    cdef void jl(self, tuple op):  # Jump if less
        if self.flags['SF'] != self.flags['OF']: self.jump(op[1])

    cdef void mov(self, tuple op): self.register[op[1]] = self.register[op[2]]


    cdef void swap(self, tuple op):
        r1 = self.register[op[1]]
        r2 = self.register[op[2]]
        self.register[op[2]] = r1
        self.register[op[1]] = r2
    cdef void dup(self, tuple op):
        s = self.stack[-1]
        self.stack.append(s)
    cdef void drop(self, tuple op):
        self.stack.pop()
    cdef void halt(self, tuple op):
        self.kill()
    cdef void rand(self, tuple op):
        cdef int num = random.randint(0, op[2])
        self.register[op[1]] = num
    cdef void inc(self, tuple op):
        self.register[op[1]]+=1
    cdef void dec(self, tuple op):
        self.register[op[1]]-=1
    cdef void abs(self, tuple op):
        self.register[op[1]] = abs(self.register[op[2]])
    cdef void neg(self, tuple op):
        self.register[op[1]] = -self.register[op[1]]
    
    cdef void change_mode(self, tuple op):
        cdef int mode = op[1]
        print("[INFO] mode changing is in developing")
        self.mode = mode



    cdef void interrupt(self, tuple op):
        cdef int interrupt = op[1]
        if interrupt == 0x45:
            self.biscuit_call()
        elif interrupt == 0x80:
            self.syscall()






    cdef void biscuit_call(self):
        cdef int call = self.register[0x2f]
        if call == 0x00:
            arg1 = self.register[0x30]
            self.exit()
        elif call == 0x01:
            hardware_memory = {}
            for i in hardware_memory_addresses:
                if self.debug:
                    print(f"[UPDATE] Updating Hardware address: {i}")
                hardware_memory[i] = self.memory[i]
            result = self.hardware.update(hardware_memory)
            self.memory.update(result)
        elif call == 0x02:
            arg1 = self.register[0x30]/1000
            time.sleep(arg1)
        elif call == 0x03:
            arg1 = self.register[0x30]
            
            result = input(arg1)
            self.register[0x2f] = result

        elif call == 0x04:
            arg1 = self.register[0x30]
            arg2 = self.register[0x31]
    
            if arg1 == 0x01:
                print(arg2)
        elif call == 0x05:
            print(f"Memory: {self.memory}")
            print(f"Stack: {self.stack}")
            print(f"Flags: {self.flags}")
            print(f"Program Counter: {self.pc}")
            print(f"Mode: {self.mode}")
            print(f"Code Sector Index: {self.code_addresses}")
        elif call == 0x06:
            arg1 = self.register[0x30]
            arg2 = self.register[0x31]
            self.fs_write_file(arg1, arg2)
        elif call == 0x07:
            arg1 = self.register[0x30]
            self.fs_read_file(arg1)
        elif call == 0x08:
            engine = Engine(data_sector={}, code_sector={}, memory_sector={}, zip=self.zip, debug=self.debug)
            engine.pc = self.pc
            engine.flags['ZF'] = 1
            engine.ret_pcs = self.ret_pcs
            engine.hardware = self.hardware
            engine.memory = self.memory
            threading.Thread(target=engine.run).start()
            self.flags['ZF'] = 0
            
        elif call == 0x09: # Get char from string (ecx) by index (ebx)
            arg1 = self.register[0x30] # Index
            arg2 = self.register[0x31] # String
             
            self.register[0x2f] = arg2[arg1]
            
    cdef void syscall(self):
        #syscall = self.register[0x2f]
        print("[INFO] Syscalls are in developing")








    cdef void fs_read_file(self, file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                self.register[0x2f] =  zip.read(file)
    cdef void fs_write_file(self, file, text):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "a", compression=zipfile.ZIP_DEFLATED) as zip:
                zip.writestr(file, text)
            
    cdef void fs_exists_file(self, file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                if file in zip.namelist():
                    self.register[0x2f] = 1
                else:
                    self.register[0x2f] = 0







    cdef void exit(self):
        raise StopEngineInterrupt

























































































    cdef void call(self, tuple op):
        self.ret_pcs.append(self.pc)
        self.jump(op[1])
    cdef void ret(self, tuple op):
        cdef int pc = self.ret_pcs.pop()
        self.pc = pc

    cdef void push(self, tuple op):
        r = self.register[op[1]]
        self.stack.append(r)
    cdef void pop(self, tuple op):
        s = self.stack.pop()
        self.register[op[1]] = s



    cdef void cmp(self, tuple op):
        r1 = op[1]
        r2 = op[2]
        val1 = self.register[r1]
        val2 = self.register[r1]
        if isinstance(val1, str) or isinstance(val2, str):
            if val1 == val2:
                self.flags['ZF'] = 1
            else:
                self.flags['ZF'] = 0
            return
        result = val1 - val2
        
        if result == 0:
            self.flags['ZF'] = 1
        else:
            self.flags['ZF'] = 0
        try:
            if result < 0:
                self.flags['SF'] = 1
            else:
                self.flags['SF'] = 0
            
            if self.register[r1] < self.register[r2]:
                self.flags['CF'] = 1
            else:
                self.flags['CF'] = 0
            
            
            if ((self.register[r1] < 0 and self.register[r2] > 0 and result > 0) or
                (self.register[r1] > 0 and self.register[r2] < 0 and result < 0)):
                self.flags['OF'] = 1
            else:
                self.flags['OF'] = 0
        except Exception as e:
            if self.debug:
                print(e)


    cdef void jump(self, int address):
        self.pc = self.code_addresses[address]-1



    

cdef class Hardware:
    cdef dict hardware_memory
    cdef dict inet_connection
    cdef object debug
    def __init__(self, debug):
        self.hardware_memory = {}
        self.debug = debug
        self.inet_connection = dict[int, socket.socket]()
    cdef dict update(self, hardware_memory): #Hardware memory is the memory of the engine with 0xFFFF####
        self.hardware_memory = hardware_memory
        self.update_color()
        self.internet()

        return self.hardware_memory

    cdef void update_color(self):
        # Change color of terminal
        # Colors are hexadezimal
        # 0xFFFF0000 Color
        color = self.hardware_memory[0xFFFF_0000]

        colors = (
            colorama.Fore.RESET,
            colorama.Fore.WHITE,
            colorama.Fore.BLACK,
            colorama.Fore.YELLOW,
            colorama.Fore.RED,
            colorama.Fore.BLUE,
            colorama.Fore.GREEN,
            colorama.Fore.MAGENTA,
            colorama.Fore.CYAN,
            colorama.Fore.LIGHTYELLOW_EX,
            colorama.Fore.LIGHTBLACK_EX,
            colorama.Fore.LIGHTCYAN_EX,
            colorama.Fore.LIGHTMAGENTA_EX,
            colorama.Fore.LIGHTGREEN_EX,
            colorama.Fore.LIGHTWHITE_EX,
            colorama.Fore.LIGHTRED_EX
        )
        color = colors[color]
        print(color, end="")
    cdef void internet(self):
        cdef int action = self.hardware_memory[0xFFFF_0100]
        if action == None:
            return
        else:
            port = int(self.hardware_memory[0xFFFF_0104])
            if action == 0x00: # Listen
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:
                    if self.debug:
                        print(f"Invalid family of socket: {fam}")
                    return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:
                    if self.debug:
                        print(f"Invalid kind of socket: {kind}")
                    return
                sock = socket.socket(fam, kind)
                sock.bind((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x01: # Connect
                fam  = self.hardware_memory[0xFFFF_0101]
                kind = self.hardware_memory[0xFFFF_0102]
                host = self.hardware_memory[0xFFFF_0103]
                if host == None:return
                if fam == 0x00: # Inet:
                    fam = socket.AF_INET
                else:
                    if self.debug:
                        print(f"Invalid family of socket: {fam}")
                    return
                if kind == 0x00: # UPD
                    kind = socket.SOCK_DGRAM
                elif kind == 0x01: # TCP
                    kind = socket.SOCK_STREAM
                else:
                    if self.debug:
                        print(f"Invalid kind of socket: {kind}")
                    return
                sock = socket.socket(fam, kind)
                sock.connect((socket.gethostbyname(host), port))
                self.inet_connection[port] = sock
            elif action == 0x02: #send
                message = self.hardware_memory[0xFFFF_0105]
                sock: socket.socket = self.inet_connection[port]
                if self.debug:
                    print(f"[SOCKET] SENDING '{message}'")
                if isinstance(message, bytes):
                    sock.send(message)
                else:
                    sock.send(bytes(message, encoding="utf8"))
            elif action == 0x03: # recv
                bufsize = self.hardware_memory[0xFFFF_0106]
                sock = self.inet_connection[port]
                msg = sock.recv(bufsize)
                self.hardware_memory[0xFFFF_0107] = msg
            elif action == 0x04: # exit
                
                self.inet_connection[port].close()
        self.hardware_memory[0xFFFF_0100] = None
                
        
        
cdef class StopEngineInterrupt(Exception):
    pass