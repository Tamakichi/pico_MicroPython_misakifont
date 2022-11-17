from misakifont import MisakiFont

"""
 フォントのビットマップ表示
"""
def show_bitmap(fd):
    for row in range(0,7):
        #print(bin(fd[row])+" ",end="")
        for col in range(0,7):
            if (0x80>>col) & fd[row]:
                print("#",end="")
            else:
                print(" ",end="")
        print()


str="123 こんにちは世界！"
mf = MisakiFont()
for c in str:
    d = mf.font(ord(c))
    show_bitmap(d)
    print()
    