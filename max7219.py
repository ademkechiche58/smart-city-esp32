import framebuf

class Matrix8x8(framebuf.FrameBuffer):
    def __init__(self, spi, cs, n):
        self.spi = spi
        self.cs = cs
        self.n = n
        self.buffer = bytearray(8 * n)
        # On utilise MONO_HLSB ou MONO_VLSB selon l'orientation voulue
        super().__init__(self.buffer, 8 * n, 8, framebuf.MONO_VLSB)
        self.init()

    def _write(self, reg, val):
        self.cs.value(0)
        for _ in range(self.n):
            self.spi.write(bytearray([reg, val]))
        self.cs.value(1)

    def init(self):
        for reg, val in ((15, 0), (11, 7), (9, 0), (12, 1)):
            self._write(reg, val)

    def brightness(self, val):
        self._write(10, val)

    def show(self):
        for y in range(8):
            self.cs.value(0)
            for m in range(self.n):
                # ICI : On ajuste l'indexation pour l'affichage horizontal
                self.spi.write(bytearray([y + 1, self.buffer[(m * 8) + y]]))
            self.cs.value(1)
