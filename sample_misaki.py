from misakifont import MisakiFont

"""
 フォントのビットマップ表示
"""
def show_bitmap(fd):
    for row in range(0,7):
        for col in range(0,7):
            print("#" if (0x80>>col) & fd[row] else " ", end="")
        print()


str="こんにちは世界！"
mf = MisakiFont()
for c in str:
    d = mf.font(ord(c))
    show_bitmap(d)
    print()
    