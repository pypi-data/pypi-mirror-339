import time
import socket
import zipfile
import threading
import random
import io
from libc.string cimport strcmp
from libc.stdio cimport printf

cdef int* hardware_memory_addresses = [
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
cdef int hardware_memory_addresses_len = 9


cdef object engine_lock_fs = threading.Lock()
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
    cdef bint debug
    cdef dict register
    cdef dict memory
    cdef dict flags
    cdef object stop_event
    cdef tuple code_memory
    """initializer"""
    def __init__(self, dict data_sector, dict code_sector, dict mem_sector, zip: io.BytesIO, bint debug=False, ):
        self.mode = 0x12
        self.zip: io.BytesIO = zip
        self.stack = []
        self.hardware = Hardware(debug)
        self.debug = debug
        self.register = {i: 0 for i in range(0x10, 0x3C)}
        self.memory = mem_sector
        self.memory.update(data_sector)


        sorted_items = sorted(code_sector.items())
        self.code_memory = tuple(value for key, value in sorted_items)
        self.code_addresses = {key: index for index, (key, value) in enumerate(sorted_items)}
        self.code_len = len(sorted_items)


        self.flags = {'ZF': 0, 'CF': 0, 'SF': 0, 'OF': 0}
        self.pc = 0
        self.ret_pcs = []
        self.stop_event = threading.Event()
        for i in range(hardware_memory_addresses_len):
            h_address = hardware_memory_addresses[i]
            self.memory[h_address] = None
    """Kill engine"""
    cpdef kill(self):
        self.stop_event.set()
    """Run"""
    cpdef run(self):

        cdef tuple op
        try:
            if self.debug:
                while self.pc < self.code_len and not self.stop_event.is_set():
                    op = self.code_memory[self.pc]
                    print("[Execute] [Address:"+hex(self.pc)+"] "+op)
                    self.execute(op)
                    self.pc += 1
            else:
                while self.pc < self.code_len and not self.stop_event.is_set():
                    op = self.code_memory[self.pc]
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


    cdef void execute(self, tuple op):
        cdef str opcode = op[0]
        cdef bytes opcode_bytes = opcode.encode('utf-8')
        cdef char* opcode_cstr = <char*>opcode_bytes
        if strcmp(opcode_cstr, b'1b') == 0:
            self.add(op)
        elif strcmp(opcode_cstr, b'1c') == 0:
            self.sub(op)
        elif strcmp(opcode_cstr, b'1d') == 0:
            self.mul(op)
        elif strcmp(opcode_cstr, b'1e') == 0:
            self.div(op)
        elif strcmp(opcode_cstr, b'1f') == 0:
            self.mod(op)
        elif strcmp(opcode_cstr, b'20') == 0:
            self.pow(op)
        elif strcmp(opcode_cstr, b'2a') == 0:
            self.and_op(op)
        elif strcmp(opcode_cstr, b'2b') == 0:
            self.or_op(op)
        elif strcmp(opcode_cstr, b'2c') == 0:
            self.xor(op)
        elif strcmp(opcode_cstr, b'2d') == 0:
            self.not_op(op)
        elif strcmp(opcode_cstr, b'2e') == 0:
            self.shl(op)
        elif strcmp(opcode_cstr, b'2f') == 0:
            self.shr(op)
        elif strcmp(opcode_cstr, b'40') == 0:
            self.load(op)
        elif strcmp(opcode_cstr, b'41') == 0:
            self.store(op)
        elif strcmp(opcode_cstr, b'42') == 0:
            self.cmp(op)
        elif strcmp(opcode_cstr, b'43') == 0:
            self.jmp(op)
        elif strcmp(opcode_cstr, b'44') == 0:
            self.je(op)
        elif strcmp(opcode_cstr, b'45') == 0:
            self.jne(op)
        elif strcmp(opcode_cstr, b'46') == 0:
            self.jg(op)
        elif strcmp(opcode_cstr, b'47') == 0:
            self.jl(op)
        elif strcmp(opcode_cstr, b'48') == 0:
            self.mov(op)
        elif strcmp(opcode_cstr, b'49') == 0:
            self.interrupt(op)
        elif strcmp(opcode_cstr, b'4a') == 0:
            self.change_mode(op)
        elif strcmp(opcode_cstr, b'4b') == 0:
            self.call(op)
        elif strcmp(opcode_cstr, b'4c') == 0:
            self.ret(op)
        elif strcmp(opcode_cstr, b'4d') == 0:
            self.push(op)
        elif strcmp(opcode_cstr, b'4e') == 0:
            self.pop(op)
        elif strcmp(opcode_cstr, b'4f') == 0:
            self.swap(op)
        elif strcmp(opcode_cstr, b'50') == 0:
            self.dup(op)
        elif strcmp(opcode_cstr, b'51') == 0:
            self.drop(op)
        elif strcmp(opcode_cstr, b'52') == 0:
            self.halt(op)
        elif strcmp(opcode_cstr, b'53') == 0:
            self.rand(op)
        elif strcmp(opcode_cstr, b'54') == 0:
            self.inc(op)
        elif strcmp(opcode_cstr, b'55') == 0:
            self.dec(op)
        elif strcmp(opcode_cstr, b'56') == 0:
            self.abs(op)
        elif strcmp(opcode_cstr, b'57') == 0:
            self.neg(op)
        else:
            printf("Unknown opcode: %s\n", opcode_cstr)


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
        printf("[INFO] mode changing is in developing\n")
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
            for i in range(hardware_memory_addresses_len):
                h_address = hardware_memory_addresses[h_address]
                if self.debug:
                    print(f"[UPDATE] Updating Hardware address: {h_address}")
                hardware_memory[h_address] = self.memory[h_address]
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
            print(f"Mode: {self.mode}", )
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
            engine.code_memory = self.code_memory
            engine.mode = self.mode
            threading.Thread(target=engine.run).start()
            self.flags['ZF'] = 0
            
        elif call == 0x09: # Get char from string (ecx) by index (ebx)
            arg1 = self.register[0x30] # Index
            arg2 = self.register[0x31] # String
             
            self.register[0x2f] = arg2[arg1]
            
    cdef void syscall(self):
        #syscall = self.register[0x2f]
        printf("[INFO] Syscalls are in developing\n")








    cdef void fs_read_file(self, str file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                self.register[0x2f] = zip.read(file)
    cdef void fs_write_file(self, str file, text):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "a", compression=zipfile.ZIP_DEFLATED) as zip:
                zip.writestr(file, text)
            
    cdef void fs_exists_file(self, str file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                if file in zip.namelist():
                    self.register[0x2f] = 1
                else:
                    self.register[0x2f] = 0







    cdef void exit(self):
        # Implement some saving features
        self.kill()

























































































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
        val2 = self.register[r2]
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
        cdef int color = self.hardware_memory[0xFFFF_0000]

        cdef const char* colors[16] 
        colors = [
            b'\033[0m',  # RESET
            b'\033[97m', # WHITE
            b'\033[30m', # BLACK
            b'\033[93m', # YELLOW
            b'\033[91m', # RED
            b'\033[94m', # BLUE
            b'\033[92m', # GREEN
            b'\033[35m', # MAGENTA
            b'\033[36m', # CYAN
            b'\033[93m', # LIGHTYELLOW
            b'\033[90m', # LIGHTBLACK
            b'\033[96m', # LIGHTCYAN
            b'\033[95m', # LIGHTMAGENTA
            b'\033[92m', # LIGHTGREEN
            b'\033[97m', # LIGHTWHITE
            b'\033[91m'  # LIGHTRED
        ]



        cdef const char * _color = colors[color]
        printf(_color)
    cdef void internet(self):
        cdef int action = self.hardware_memory[0xFFFF_0100]
        cdef int port
        cdef int kind
        cdef int fam
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
                        print(f"Invalid kind of socket: {kind}", kind)
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