from misakifont import MisakiFont

def banner(text, fc="#", bc=" "):

    # 美咲フォントのインスタンス生成
    mf = MisakiFont()
  
    # 文字列のフォントパータンをバッファに格納
    buf = []
    for char in text:
        code = ord(char)
        fontdata = mf.font(code, False)
        width = 8 if mf.isZenkaku(code) else 4
        for w in range(width):
            data = 0        
            for row in range(8):
                if fontdata[row] & 0x80 >> w:
                    data |= (0x80 >> row)
            buf.append(data)

    # バッファのデータの表示
    for row in range(8):
        for i in range(len(buf)):
            print(fc if buf[i] & (0x80>>row) else bc, end='')
        print()

banner("AbあAaこんばんはー１×2")
banner("12345今日は", "*")
            
    