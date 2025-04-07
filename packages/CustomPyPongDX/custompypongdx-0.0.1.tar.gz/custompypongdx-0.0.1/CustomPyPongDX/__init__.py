from CustomPyPongDX import Pong

class Font:
    def __init__(self, fontfile):
        self.font = fontfile

    def useFont(self):
        return self.font

class Color:
    def __init__(self, colorstr):
        self.color = colorstr

    def useColor(self):
        return self.color


class Music:
    def __init__(self, musfile):
        self.music = musfile

    def useMusicFile(self):
        return self.music

class PingPong:
    def __init__(self, font, colorR, colorL,
                 bgcolor, music, susound,
                 aisoundL, aisoundR, pongSound, matchpoint):
        Pong.CreatePing(font, colorR, colorL,
                        bgcolor, music, susound,
                 aisoundL, aisoundR, pongSound, matchpoint)

