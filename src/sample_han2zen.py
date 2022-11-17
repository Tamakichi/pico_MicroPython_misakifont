# 半角全角変換テスト
from misakifont import MisakiFont

mf = MisakiFont()
for code in range(0x20,0x7F):
    print(chr(code),"=>",chr(mf.han2zen(code)))

for code in range(0xff50,0xffa0):
    print(chr(code),"=>",chr(mf.han2zen(code)))


