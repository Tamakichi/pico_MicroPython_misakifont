"""日本語文字(ユニコード)処理ユーティリティ for MicroPython v1.10

  [履歴]
  2022/11/18, ユーティリティの作成, たま吉さん  
  2024/03/08, isBasicLatin()、isLatinSupple(),LatenS2Zen()の追加、不具合対応, たま吉さん  
"""

# 半角カナ全角変換テーブル
#  全角コード = kana_h2z_map[code-0xff61] + 0x3000
kana_h2z_map = (
    0x02,0x0c,0x0d,0x01,0xfb,0xf2,0xa1,0xa3,
    0xa5,0xa7,0xa9,0xe3,0xe5,0xe7,0xc3,0xfc,
    0xa2,0xa4,0xa6,0xa8,0xaa,0xab,0xad,0xaf,
    0xb1,0xb3,0xb5,0xb7,0xb9,0xbb,0xbd,0xbf,
    0xc1,0xc4,0xc6,0xc8,0xca,0xcb,0xcc,0xcd,
    0xce,0xcf,0xd2,0xd5,0xd8,0xdb,0xde,0xdf,
    0xe0,0xe1,0xe2,0xe4,0xe6,0xe8,0xe9,0xea,
    0xeb,0xec,0xed,0xef,0xf3,0x9b,0x9c,
)

"""基本ラテン文字判定

    指定した文字コードが0x20～0x7eの場合True、そうでない場合Falseを返す
    引数 ucode: UTF-16 コード

"""
def isBasicLatin(ucode):
    return (ucode >=0x20) and (ucode <= 0x7e)


"""ラテン1補助判定

    指定した文字コードが0x20～0x7eの場合True、そうでない場合Falseを返す
    引数 ucode: UTF-16 コード

"""
def isLatinSupple(ucode):
    return (ucode >=0xa1) and (ucode <= 0xff)


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
    return kana_h2z_map[ucode - 0xFF61] + 0x3000 if (isHkana(ucode)) else ucode

"""半角ラテン1補助全角文字変換(美咲フォント用)
       
    指定した半角ラテン1補助文字に対応する全角文字コードを返す
    引数 ucode: UTF-16 コード
    戻り値： 全角カタカナコード（半角ラテン1補助文字コードでない場合はそのまま返す）

    ※本関数は利用しているフォントに依存する('¢', '£', '¥', '¦', '¬', '¯')

"""
def LatenS2Zen(ucode):
    c = {0xa2:0xffe0, 0xa3:0xffe1, 0xa5:0xffe5, 0xa6:0xffe4,
         0xac:0xffe2, 0xaf:0xffe3,}.get(ucode)
    return c if c != None else  ucode

"""半角文字コード・全角文字コード変換

  引数   ucode UTF-16 コード
  戻り値: 変換コード（ 変換できない場合は元のコードを返す)
"""
def han2zen(ucode, fncLatenS2Zen=LatenS2Zen):
    if ucode == 0x20:            # 全角スペース文字
        return 0x3000
    elif isBasicLatin(ucode):   # 基本ラテン文字
        return ucode - 0x20 + 0xff00
    elif isLatinSupple(ucode):  # ラテン1補助
        return fncLatenS2Zen(ucode)
    elif isHkana(ucode):        # 半角カタカナ
        return hkana2kana(ucode)
    return ucode


"""全角・半角判定

  引数   ucode UTF-16 コード
  戻り値: 半角幅 False、全角幅 True
"""
def isZenkaku(ucode):
    if isBasicLatin(ucode):               # 基本ラテン文字
        return False 
    elif isLatinSupple(ucode):            # ラテン1補助
        return True if ucode in (0xa7,0xa8,0xad,0xb0,0xb1,0xb4,0xb6,0xd7,0xf7) else False
    elif isHkana(ucode):                  # 半角カタカナ
        return False 
    elif ucode < 0x20:                    #C0
        return False         
    elif ucode >= 0x7f and ucode <= 0xa0: #C1
        return False        
    return True                          # その他


"""リスト内２分検索

  指定したリストの二分探索を行い、該当するデータのある位置を返す
  引数   コード
         データ数
         検索対象データ取得関数
  戻り値 該当フォントがある場合 インデックス番号(0～テーブルサイズ-1)
        該当フォントが無い場合 -1
"""
def binfind(code, n, get_at):
    t_p = 0;                  # 検索範囲上限
    e_p = n-1                 # 検索範囲下限
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
    for code in range(0x20,0xff):
        print(code,hex(code),
              chr(code),
              "1" if isZenkaku(code) else "0",
              han2zen(code),
              hex(han2zen(code)),
              chr(han2zen(code)),
              "1" if isZenkaku(han2zen(code)) else "0",
              sep=",")

    for code in range(0xff61,0xffa0):
        print(code,hex(code),
              chr(code),
              "1" if isZenkaku(code) else "0",
              han2zen(code),
              hex(han2zen(code)),
              chr(han2zen(code)),
              "1" if isZenkaku(han2zen(code)) else "0",
              sep=",")
