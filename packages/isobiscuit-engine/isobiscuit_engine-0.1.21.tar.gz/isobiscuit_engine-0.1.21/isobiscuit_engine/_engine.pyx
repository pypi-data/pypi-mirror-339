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
    cdef list register
    cdef dict memory
    cdef dict flags
    cdef object stop_event
    cdef tuple code_memory
    """initializer"""
    def __init__(self, dict data_sector, dict code_sector, dict mem_sector, zip: io.BytesIO, bint debug=False, ):
        self.mode = 0x12
        self.zip: io.BytesIO = zip
        self.stack = []
        
        self.debug = debug
        self.register = [None for i in range(0x0, 0x3c)]
        self.memory = mem_sector
        self.memory.update(data_sector)
        self.hardware = Hardware(self.memory, debug)
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
                while self.running_conditions():
                    op = self.code_memory[self.pc]
                    print("[Execute] [Address:"+hex(self.pc)+"] "+op)
                    self.execute(op)
                    self.pc += 1
            else:
                while self.running_conditions():
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

    cdef bint running_conditions(self):
        return (self.pc < self.code_len and not self.stop_event.is_set())
    cdef void execute(self, tuple op):
        cdef unsigned char opcode = int(op[0], 16)

        if opcode == 0x1b:
            self.add(op)
        elif opcode == 0x1c:
            self.sub(op)
        elif opcode == 0x1d:
            self.mul(op)
        elif opcode == 0x1e:
            self.div(op)
        elif opcode == 0x1f:
            self.mod(op)
        elif opcode == 0x20:
            self.pow(op)
        elif opcode == 0x2a:
            self.and_op(op)
        elif opcode == 0x2b:
            self.or_op(op)
        elif opcode == 0x2c:
            self.xor(op)
        elif opcode == 0x2d:
            self.not_op(op)
        elif opcode == 0x2e:
            self.shl(op)
        elif opcode == 0x2f:
            self.shr(op)
        elif opcode == 0x40:
            self.load(op)
        elif opcode == 0x41:
            self.store(op)
        elif opcode == 0x42:
            self.cmp(op)
        elif opcode == 0x43:
            self.jmp(op)
        elif opcode == 0x44:
            self.je(op)
        elif opcode == 0x45:
            self.jne(op)
        elif opcode == 0x46:
            self.jg(op)
        elif opcode == 0x47:
            self.jl(op)
        elif opcode == 0x48:
            self.mov(op)
        elif opcode == 0x49:
            self.interrupt(op)
        elif opcode == 0x4a:
            self.change_mode(op)
        elif opcode == 0x4b:
            self.call(op)
        elif opcode == 0x4c:
            self.ret(op)
        elif opcode == 0x4d:
            self.push(op)
        elif opcode == 0x4e:
            self.pop(op)
        elif opcode == 0x4f:
            self.swap(op)
        elif opcode == 0x50:
            self.dup(op)
        elif opcode == 0x51:
            self.drop(op)
        elif opcode == 0x52:
            self.halt(op)
        elif opcode == 0x53:
            self.rand(op)
        elif opcode == 0x54:
            self.inc(op)
        elif opcode == 0x55:
            self.dec(op)
        elif opcode == 0x56:
            self.abs(op)
        elif opcode == 0x57:
            self.neg(op)
        else:
            printf("Unknown opcode: 0x%02x\n", opcode)


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
            result = self.hardware.update()
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
        engine_lock_fs.acquire()
        
        try:
            z = zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED)
            self.register[0x2f] = z.read(file)  
        finally:
            engine_lock_fs.release()
            z.close()

    cdef void fs_write_file(self, str file, text):
        engine_lock_fs.acquire()
        
        try:
            z = zipfile.ZipFile(self.zip, "a", compression=zipfile.ZIP_DEFLATED)
            z.writestr(file, text) 
        finally:
            engine_lock_fs.release()
            z.close()
            
    cdef void fs_exists_file(self, str file):
        engine_lock_fs.acquire()
        
        try:
            z = zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED)
            if file in z.namelist():
                self.register[0x2f] = 1
            else:
                self.register[0x2f] = 0 
        finally:
            engine_lock_fs.release()
            z.close()






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
    def __init__(self, dict memory, debug):
        self.hardware_memory = memory
        self.hardware_memory[0xFFFF_0100] == 99
        self.debug = debug
        self.inet_connection = dict[int, socket.socket]()
    cdef dict update(self): #Hardware memory is the memory of the engine with 0xFFFF####
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
        if action == 99:
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
        self.hardware_memory[0xFFFF_0100] = 99
                   
        
cdef class StopEngineInterrupt(Exception):
    pass