# ssd1306.py
import framebuf
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3c):
        self.i2c = i2c
        self.addr = addr
        self.width = width
        self.height = height
        self.buffer = bytearray(((height // 8) * width))
        super().__init__(self.buffer, width, height, framebuf.MONO_VLSB)
        self.init_display()
    def init_display(self):
        for cmd in (0xae, 0x20, 0x10, 0x40, 0x81, 0xff, 0xa1, 0xa6, 0xa8, 0x3f, 0xd3, 0x00, 0xd5, 0x80, 0xd9, 0xf1, 0xda, 0x12, 0xdb, 0x40, 0x8d, 0x14, 0xaf):
            self.i2c.writeto_mem(self.addr, 0, bytearray([cmd]))
    def show(self):
        self.i2c.writeto_mem(self.addr, 0x40, self.buffer)