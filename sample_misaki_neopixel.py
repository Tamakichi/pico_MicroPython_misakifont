"""
Neopixel 8x8ドットマトリックス 美咲フォント表示デモ

"""
from time import sleep_ms
from random import randint
from misakifont import MisakiFont
from device.neomatrix import NeoMatrix

pin = 26
maxBright = 15

str="12abcこんにちは,世界! ｺﾝﾆﾁﾊｾｶｲ!"
np = NeoMatrix(pin)
mf = MisakiFont()
np.cls()

while True:
    #矩形の表示
    for i in range(5):
        color = [randint(0, maxBright) for n in range(3)]
        for j in range(0, 4):
            np.cls(False)
            np.line(j, j, 7-j, 7-j, color, 1)
            sleep_ms(150)

    #文字のスクロール表示
    for c in str:
        d = mf.font(ord(c),False)
        color = [randint(0, maxBright) for n in range(3)]
        np.scrollIn(d, color,100, fw = 8 if mf.isZenkaku(ord(c)) else 4)
    sleep_ms(1000)
    np.cls()
