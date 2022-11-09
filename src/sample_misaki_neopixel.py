"""
Neopixel 8x8ドットマトリックス 美咲フォント表示デモ

"""
from misakifont import MisakiFont
from machine import Pin
from neopixel import NeoPixel
import time
import random
from neomatrix import NeoMatrix

pin = 26

str="こんにちは世界！"
np = NeoMatrix(pin)
mf = MisakiFont()
np.cls()

while True:
    #矩形の表示
    for i in range(5):
        color = (random.randint(0, 50),random.randint(0, 50),random.randint(0, 50))
        for j in range(0,4):
            np.cls(False)
            np.line(j,j,7-j,7-j,color,1)
            time.sleep_ms(150)

    #文字のスクロール表示
    for c in str:
        d = mf.font(ord(c))
        color = (random.randint(0, 50),random.randint(0, 50),random.randint(0, 50))
        np.scrollIn(d,color,100)
    time.sleep_ms(1000)
    np.cls()
