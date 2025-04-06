import colorama
import time
import socket
import zipfile
import io
import copy
import threading
import random



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

class Engine:
    def __init__(self, data_sector, code_sector, mem_sector, zip: io.BytesIO, debug=False, ):
        self.mode = "biscuit"
        self.zip: io.BytesIO = zip
        self.stack = []
        self.hardware = Hardware(debug)
        self.debug = debug
        self.register = {i: 0 for i in range(0x10, 0x3C)}
        self.memory = {**mem_sector,**data_sector, **code_sector}
        self.flags = {'ZF': 0, 'CF': 0, 'SF': 0, 'OF': 0}
        self.pc = 0
        self.code_addresses = list(code_sector.keys())
        self.code_len = len(self.code_addresses)
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
    def kill(self):
        self.stop_event.set()
    def run(self):
        try:
            while self.pc < self.code_len and not self.stop_event.is_set():
                address = self.code_addresses[self.pc]
                op = self.memory[address]
                if self.debug:
                    print(f"[Execute] [Address:{hex(address)}] {op}")
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
    def execute(self, op):
        opcode: str = op[0]
        if opcode in self.OPCODES:
            self.OPCODES[opcode](op) 
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def add(self, op): self.register[op[1]] += self.register[op[2]]
    def sub(self, op): self.register[op[1]] -= self.register[op[2]]
    def mul(self, op): self.register[op[1]] *= self.register[op[2]]
    def div(self, op): self.register[op[1]] //= self.register[op[2]]
    def mod(self, op): self.register[op[1]] %= self.register[op[2]]
    def pow(self, op): self.register[op[1]] **= self.register[op[2]]

    def and_op(self, op): self.register[op[1]] &= self.register[op[2]]
    def or_op(self, op): self.register[op[1]] |= self.register[op[2]]
    def xor(self, op): self.register[op[1]] ^= self.register[op[2]]
    def not_op(self, op): self.register[op[1]] = ~self.register[op[1]]
    def shl(self, op): self.register[op[1]] <<= op[2]
    def shr(self, op): self.register[op[1]] >>= op[2]

    def load(self, op): self.register[op[1]] = self.memory[op[2]]
    def store(self, op): self.memory[op[2]] = self.register[op[1]]

    def jmp(self, op): self.jump(op[1])
    def je(self, op):  # Jump if equal
        if self.flags['ZF']: self.jump(op[1])
    def jne(self, op):  # Jump if not equal
        if not self.flags['ZF']: self.jump(op[1])
    def jg(self, op):  # Jump if greater
        if not self.flags['ZF'] and self.flags['SF'] == self.flags['OF']: self.jump(op[1])
    def jl(self, op):  # Jump if less
        if self.flags['SF'] != self.flags['OF']: self.jump(op[1])

    def mov(self, op): self.register[op[1]] = self.register[op[2]]


    def swap(self, op):
        r1 = self.register[op[1]]
        r2 = self.register[op[2]]
        self.register[op[2]] = r1
        self.register[op[1]] = r2
    def dup(self, op):
        s = self.stack[-1]
        self.stack.append(s)
    def drop(self, op):
        self.stack.pop()
    def halt(self, op):
        self.kill()
    def rand(self, op):
        num = random.randint(0, op[2])
        self.register[op[1]] = num
    def inc(self, op):
        self.register[op[1]]+=1
    def dec(self, op):
        self.register[op[1]]-=1
    def abs(self, op):
        self.register[op[1]] = abs(self.register[op[2]])
    def neg(self, op):
        self.register[op[1]] = -self.register[op[1]]
    
    def change_mode(self, op):
        mode = op[1]
        print("[INFO] mode changing is in developing")
        self.mode = mode



    def interrupt(self, op):
        interrupt = op[1]
        if interrupt == 0x45:
            self.biscuit_call()
        elif interrupt == 0x80:
            self.syscall()






    def biscuit_call(self):
        call = self.register[0x2f]
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
            arg1 :int = self.register[0x30] # Index
            arg2 :str = self.register[0x31] # String
             
            self.register[0x2f] = arg2[arg1]
            
    def syscall(self):
        #syscall = self.register[0x2f]
        print("[INFO] Syscalls are in developing")








    def fs_read_file(self, file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                self.register[0x2f] =  zip.read(file)
    def fs_write_file(self, file, text):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "a", compression=zipfile.ZIP_DEFLATED) as zip:
                zip.writestr(file, text)
            
    def fs_exists_file(self, file):
        with engine_lock_fs:
            with zipfile.ZipFile(self.zip, "r", compression=zipfile.ZIP_DEFLATED) as zip:
                if file in zip.namelist():
                    self.register[0x2f] = 1
                else:
                    self.register[0x2f] = 0







    def exit(self):
        raise StopEngineInterrupt

























































































    def call(self, op):
        self.ret_pcs.append(self.pc)
        self.jump(op[1])
    def ret(self, op):
        pc = self.ret_pcs.pop()
        self.pc = pc

    def push(self, op):
        r = self.register[op[1]]
        self.stack.append(r)
    def pop(self, op):
        s = self.stack.pop()
        self.register[op[1]] = s



    def cmp(self, op):
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


    def update_register(self, register: int, value):
        if register > 0xf and register < 0x2a:
            self.register[register] = bool(value)
        else:
            self.register[register] = value
    def jump(self, address):
        self.pc = self.code_addresses.index(address)-1


    def _update_1bit_register(self, register: int, value: bool):
        register[register] = value
    
    def _update_register(self, register: int, value):
        register[register] = value


    

class Hardware:
    def __init__(self, debug):
        self.hardware_memory = {}
        self.debug = debug
        self.inet_connection = dict[int, socket.socket]()
    def update(self, hardware_memory): #Hardware memory is the memory of the engine with 0xFFFF####
        self.hardware_memory = hardware_memory
        self.update_color()
        self.internet()

        return self.hardware_memory

    def update_color(self):
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
    def internet(self):
        action = self.hardware_memory[0xFFFF_0100]
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
                bufsize: int = self.hardware_memory[0xFFFF_0106]
                sock = self.inet_connection[port]
                msg = sock.recv(bufsize)
                self.hardware_memory[0xFFFF_0107] = msg
            elif action == 0x04: # exit
                
                self.inet_connection[port].close()
        self.hardware_memory[0xFFFF_0100] = None
                
        
        
class StopEngineInterrupt(Exception):
    pass