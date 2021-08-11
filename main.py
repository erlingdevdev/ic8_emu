import pygame

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
    processor.load("IBM.ch8")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        processor.fetch()
        processor.decode()
        display.draw(10, 10)
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

    def draw(self, x, y):
        x = x*self.scale
        y = y*self.scale

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (x, y, self.scale, self.scale))

    def clearsc(self):
        self.screen.fill((0, 0, 0))


class Proc():
    def __init__(self, screen, width, height, scale):
        self.screen = screen
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
            0x6: self.set_register,
            0x7: self.add_value,
            0xA: self.set_idxreg,
            0xD: self.draw,
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
        # print(hex(self.opcode))
        self.instructions[(self.opcode & 0xf000) >> 12]()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def zero_subroutines(self):
        operation = self.opcode & 0x00ff
        if(operation == 0x00e0):
            self.clear_screen()

    def jump(self):
        val = self.opcode & 0x0fff
        self.registers["pc"] = val

    def set_register(self):
        target = (self.opcode & 0x0F00) >> 8
        self.registers['V'][target] = self.opcode & 0x00FF

    def load(self, file):
        data = open(file, "rb").read()
        print(data)
        for i in range(0, len(font)):
            self.mem[i] = font[i]

        for i, val in enumerate(data):
            self.mem[0x200 + i] = val

    def add_value(self):
        register = self.get_x()
        self.registers["V"][register] = self.opcode & 0x00FF

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

        for y in range(nbytes):
            pixel = self.mem[self.registers["I"] + y]
            y_pos = y_pos %
            print(hex(pixel))
            for x in range(8):
                if (pixel and (0x80 >> x)):
                    pass

    def get_y(self):
        return (self.opcode & 0x00f0) >> 4


if __name__ == "__main__":
    main()
