"""日本語文字(ユニコード)処理ユーティリティ for MicroPython v1.00

  [履歴]
  2022/11/18, ユーティリティの作成, たま吉さん  
"""

"""半角カタカナ文字判定

    指定した文字コードが半角カタカナの場合、True、そうでない場合Falseを返す
    引数 ucode: UTF-16 コード
"""
def isHkana(ucode):
    return (ucode >=0xFF61) and (ucode <= 0xFF9F)


"""半角カタカナ全角文字変換
       
    指定した半角カタカナコードに対応する全角カタカナコードを返す
    引数 ucode: UTF-16 コード
    戻り値： 全角カタカナコード（半角カタカナコードでない場合はそのまま返す）
"""
def hkana2kana(ucode):
    # 半角カナ全角変換テーブル
    kana_h2z_map = (
        0x02,0x0C,0x0D,0x01,0xFB,0xF2,0xA1,0xA3,0xA5,0xA7,0xA9,0xE3,0xE5,0xE7,0xC3,0xFD,
        0xA2,0xA4,0xA6,0xA8,0xAA,0xAB,0xAD,0xAF,0xB1,0xB3,0xB5,0xB7,0xB9,0xBB,0xBD,0xBF,
        0xC1,0xC4,0xC6,0xC8,0xCA,0xCB,0xCC,0xCD,0xCE,0xCF,0xD2,0xD5,0xD8,0xDB,0xDE,0xDF,
        0xE0,0xE1,0xE2,0xE4,0xE6,0xE8,0xE9,0xEA,0xEB,0xEC,0xED,0xEF,0xF3,0x9B,0x9C  
    )
    return kana_h2z_map[ucode - 0xFF61] + 0x3000 if (isHkana(ucode)) else ucode


"""半角文字コード・全角文字コード変換

  引数   ucode UTF-16 コード
  戻り値: 変換コード（ 変換できない場合は元のコードを返す)
"""
def han2zen(ucode):
    ucode = hkana2kana(ucode)
    if ucode > 0xff or ucode < 0x20: 
        return ucode
    if ucode in (0x5C,0xA2,0xA3,0xA7,0xA8,0xAC,0xB0,0xB1,0xB4,0xB6,0xD7,0xF7):
        return ucode
    else:
        c = { 
            0x20:0x3000, 0x21:0xFF01, 0x22:0x201D, 0x23:0xFF03, 0x24:0xFF04, 
            0x25:0xFF05, 0x26:0xFF06, 0x27:0x2019, 0x28:0xFF08, 0x29:0xFF09,
            0x2A:0xFF0A, 0x2B:0xFF0B, 0x2C:0xFF0C, 0x2D:0x2212, 0x2E:0xFF0E,       
        }.get(ucode)
        
        if c != None:
            return c
    return  ucode - 0x2F +  0xFF0F


"""リスト内２分検索

　　指定したリストの二分探索を行い、該当するデータのある位置を返す
  引数   コード
         データ数
         検索対象データ取得関数
  戻り値 該当フォントがある場合 インデックス番号(0～テーブルサイズ-1)
        該当フォントが無い場合 -1
"""
def binfind(code, n, get_at):
    t_p = 0;                  #　検索範囲上限
    e_p = n-1                 #  検索範囲下限
    flg_stop = 0
    d = None
    
    while(True):
        pos = t_p + ((e_p - t_p+1)>>1)
        d = get_at(pos)
        if d == code:      # 等しい
            flg_stop = 1    
            break
        elif code > d:     # 大きい
            t_p = pos + 1   
            if t_p > e_p:
                break
        else:              # 小さい
            e_p = pos -1
            if e_p < t_p:
                break
    if not flg_stop:
        return -1
    return pos

# 動作確認
if __name__ == "__main__":
    for code in range(0x20,0x7F):
        print(chr(code),"=>",chr(han2zen(code)))

    for code in range(0xff50,0xffa0):
        print(chr(code),"=>",chr(han2zen(code)))
