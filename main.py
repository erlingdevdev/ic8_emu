import pygame, random

scale = 20
res = width, height = 64 * scale, 32 * scale
memory = 4096


font = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
        0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
        0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
        0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
        0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
        0xF0, 0x80, 0xF0, 0x80, 0x80]  # F


def main():
    pygame.init()
    pygame.display.set_caption("!g")
    display = Display()
    display.init()
    processor = Proc(display, width, height, scale)
    processor.load("tetris.ch8")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        processor.fetch()
        processor.decode()
        # display.draw(10, 10)
        display.update()


class Display:
    def __init__(self):

        self.scale = 20
        self.width = 64
        self.height = 32
        self.res = (self.width*self.scale, self.height*self.scale)
        self.screen = None

    def init(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode(res)
        self.clearsc()
        self.update()

    @staticmethod
    def update():
        pygame.display.flip()

    def draw(self, x, y,color=1):
        x = x*self.scale
        y = y*self.scale


        pygame.draw.rect(self.screen, (255, 255, 255) if color else (0,0,0),
                         (x, y, self.scale, self.scale))

    def get_pixel(self,x,y):
        x = x*self.scale
        y = y*self.scale
        pixel = self.screen.get_at((x,y))
        if pixel == (255,255,255):
            return 1
        else:
            return 0

    def clearsc(self):
        self.screen.fill((0, 0, 0))


class Proc():
    def __init__(self, screen, width, height, scale):
        self.Display = screen
        self.width = width
        self.height = height
        self.scale = scale
        self.res = (self.width*self.scale, self.height*self.scale)
        self.mem = bytearray(4096)
        self.opcode = 0x0
        self.running = True
        self.registers = {"sp": 0x0, "pc": 0x200, "I": 0x0, "V": [0] * 0x10, }
        self.instructions = {
            0x0: self.zero_subroutines,
            0x1:  self.jump,
            0x2: self.jump_to,
            0x3: self.skip,
            0x4: self.skip,
            0x5: self.skip,
            0x6: self.set_register,
            0x7: self.add_value,
            0x8: self.logical_operator,
            0x9 : self.skip,
            0xA: self.set_idxreg,
            0xB: self.jump_to_idx_w_val,
            0xC: self.random,
            0xD: self.draw,
            0xE: self.keyboard_routines,
            0xF: self.misc,
        }

    def fetch(self):
        pc = self.registers["pc"] = self.registers["pc"]
        opcode = self.mem[pc] << 8 | self.mem[pc+1]
        self.opcode = opcode
        self.registers["pc"] += 2

    def decode(self):
        """
        00e0 clear
        1nnn jmp
        6xnn set reg VX
        7xnn add to vx
        Annn set idx reg i
        Dxyn display
        """
        print(hex(self.opcode))
        self.instructions[(self.opcode & 0xf000) >> 12]()

    def skip(self):
        op = (self.opcode & 0xf000) >> 12
        match op :
            case 0x3:
                src = (self.opcode & 0x0f00) >> 8
                if self.registers["V"][src] is (self.opcode & 0x00ff):
                    self.registers["pc"] +=2
            case 0x4:
                src = (self.opcode & 0x0f00) >> 8
                if self.registers["V"][src] is not(self.opcode & 0x00ff):
                    self.registers["pc"] +=2
            case 0x5:
                src = (self.opcode & 0x0f00) >>8
                target = (self.opcode & 0x00f0) >> 4
                if self.registers["V"][src] is self.registers["V"][target]:
                    self.registers["pc"] +=2

    def clear_screen(self):
        self.Display.clearsc()

    def zero_subroutines(self):
        operation = self.opcode & 0x00ff
        match operation :
            case 0x00e0:
                self.clear_screen()

        if(operation == 0x00e0):
            self.clear_screen()

    def jump_to(self):
        self.mem[self.registers["sp"]] = self.registers["pc"] & 0x00ff
        self.registers["sp"] +=1
        self.mem[self.registers["sp"]] = (self.registers["pc"] & 0xff00) >> 8
        self.registers["sp"] +=1
        self.registers["pc"] = self.opcode & 0x0FFF


    def jump(self):
        val = self.opcode & 0x0fff
        self.registers["pc"] = val
    def jump_to_idx_w_val(self):
        self.registers["pc"] = self.registers["I"] + (self.opcode & 0x0fff)

    def random(self):
        target = self.get_target()
        val = self.get_value

        self.registers["V"][target] = val & random.randint(0,255)

    def keyboard_routines(self):

        pass

    def misc(self):
        pass

    def set_register(self):
        target = (self.opcode & 0x0F00) >> 8
        self.registers['V'][target] = self.opcode & 0x00FF

    def get_value(self):
        return self.opcode & 0x00ff

    def get_target(self):
        return (self.opcode & 0x0f00) >> 8
    def get_src(self):
        return (self.opcode & 0x00f0) >> 4

    def logical_operator(self):
        op = self.opcode & 0x000f
        target = self.get_target()
        source = self.get_src()
        match op:
            case 0x0:
                self.registers["V"][target] = self.registers["V"][source]
            case 0x1:
                self.registers["V"][target] |= self.registers["V"][source]
            case 0x2:
                self.registers["V"][target] &= self.registers["V"][source]
            case 0x3:
                self.registers["V"][target] ^= self.registers["V"][source]
            case 0x4:
                add = self.registers["V"][target] + self.registers["V"][source]
                if add > 255:
                    self.registers["V"][target] = add - 256
                    self.registers["V"][0xf] = 1
                else:
                    self.registers["V"][target] = add
                    self.registers["V"][0xf] = 0

            case 0x5:
                reg_t = self.registers["V"][target]
                reg_s = self.registers["V"][source]
                if reg_t > reg_s:
                    self.registers["V"][target] -= reg_s
                    self.registers["V"][0xf]= 1
                else:
                    self.registers["V"][target] = 256 + reg_t - reg_s
                    self.registers["V"][0xf]= 0
            case 0x6:
                zeros = self.registers["V"][source] & 0x1
                self.registers["V"][target] = self.registers["V"][source] >> 1
                self.registers["V"][0xF] = zeros

            case 0x7:
                reg_t = self.registers["V"][target]
                reg_s = self.registers["V"][source]
                if reg_s > reg_t:
                    self.registers["V"][target] = reg_s - reg_t
                    self.registers["V"][0xf]= 1
                else:
                    self.registers["V"][target] = 256 + reg_s - reg_t
                    self.registers["V"][0xf]= 0
            case 0xE:
                seventh = (self.registers["V"][source] & 0x80) >> 8
                self.registers["V"][target] = self.registers["V"][source] << 1
                self.registers["V"][0xF] = seventh 

    def load(self, file):
        data = open(file, "rb").read()
        print(data)
        for i in range(0, len(font)):
            self.mem[i] = font[i]

        for i, val in enumerate(data):
            self.mem[0x200 + i] = val

    def add_value(self):
        register = self.get_x()

        self.registers["V"][register] +=  self.opcode & 0x00ff

    def get_x(self):
        return (self.opcode & 0x0f00) >> 8

    def set_idxreg(self):
        val = self.opcode & 0x0fff
        self.registers["I"] = val

    def draw(self):
        register_x = self.get_x()
        register_y = self.get_y()
        x_pos = self.registers["V"][register_x]
        y_pos = self.registers["V"][register_y]
        nbytes = self.opcode & 0x000f
        self.registers['V'][0xF] = 0

        for y in range(nbytes):
            pixel = bin(self.mem[self.registers["I"] + y])
            pixel = pixel[2:].zfill(8)

            y_coord = y_pos + y
            y_coord = y_coord % self.height

            for x in range(8):
                pix = int(pixel[x])
                x_coord = x_pos + x
                x_coord = x_coord % self.width

                curr = self.Display.get_pixel(x_coord,y_coord)
                if pix and curr:
                    self.registers["V"][0xf] = self.registers["V"][0xf] | 1
                    pix = 0
                elif not pix and curr:
                    pix = 1
                print(x_coord,y_coord)
                self.Display.draw(x_coord,y_coord,pix)

    def get_y(self):
        return (self.opcode & 0x00f0) >> 4


if __name__ == "__main__":
    main()
