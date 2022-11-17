from misakifontdata import misaki_font_data, misaki_font_table, kana_h2z_map

"""美咲フォント 8x8ドット教育漢字＋非漢字 1710文字 利用クラスライブラリ for MicroPison"""
class MisakiFont:
    FTABLESIZE =   len(misaki_font_table)     # フォントテーブルデータサイズ
    FONT_LEN   =   7                          # 1フォントのバイト数
    FONT_TOFU  =   0x25a1                     # 豆腐"□"コード

    def __init__(self):
        pass

    """フォントコード検索

      引数   ucode UTF-16 コード
      戻り値 該当フォントがある場合 フォントコード(0～FTABLESIZE-1)
            該当フォントが無い場合 -1
    """
    def find(self, ucode):
        t_p = 0;                 #　検索範囲上限
        e_p = self.FTABLESIZE-1  #  検索範囲下限
        flg_stop = 0
        d = None
        
        while(True):
            pos = t_p + ((e_p - t_p+1)>>1)
            d = misaki_font_table[pos]
            if d == ucode:      # 等しい
                flg_stop = 1    
                break
            elif ucode > d:     # 大きい
                t_p = pos + 1   
                if t_p > e_p:
                    break
            else:               # 小さい
                e_p = pos -1
                if e_p < t_p:
                    break
        if not flg_stop:
            return -1
        return pos

    """半角カナ文字判定
    
      引数   ucode UTF-16 コード
    """
    def isHkana(self, ucode):
        return (ucode >=0xFF61) and (ucode <= 0xFF9F)

    """半角カナ全角文字変換

      引数   ucode UTF-16 コード
    """
    def hkana2kana(self, ucode):
        if (self.isHkana(ucode)):
            return chr(kana_h2z_map[ucode - 0xFF61] + 0x3000)
        return ucode

    """UTF16半角文字コードをUTF16全角文字コードに変換する

       (変換できない場合は元のコードを返す)
       引数   ucode UTF-16 コード
       戻り値: 変換コード
    """
    def han2zen(self, ucode):
        utf16Code = self.hkana2kana(ucode)
        if ucode > 0xff or ucode < 0x21: 
            return ucode
        if utf16Code in (0x5C,0xA2,0xA3,0xA7,0xA8,0xAC,0xB0,0xB1,0xB4,0xB6,0xD7,0xF7):
            return ucode
        else:
            c = { 
                0x21:0xFF01, 0x22:0x201D, 0x23:0xFF03, 0x24:0xFF04, 0x25:0xFF05,
                0x26:0xFF06, 0x27:0x2019, 0x28:0xFF08, 0x29:0xFF09, 0x2A:0xFF0A,
                0x2B:0xFF0B, 0x2C:0xFF0C, 0x2D:0x2212, 0x2E:0xFF0E,       
            }.get(ucode)
            
            if c != None:
                return c
        return  ucode - 0x2F +  0xFF0F     

    """UTF16文字コードに対応する美咲フォントデータ8バイトを取得する

       引数   ucode UTF-16 コード
       戻り値: 正常終了 取得したデータ(トプル) 、異常終了 None
    """
    def font(self,utf16,flgz=True):
        if flgz:
            utf16 = self.han2zen(utf16)
        code  = self.find(utf16)
        if code < 0: # 該当するフォントが存在しない
            code = self.find(self.FONT_TOFU)
        return misaki_font_data[code*self.FONT_LEN:code*self.FONT_LEN+self.FONT_LEN] + (0,) 
