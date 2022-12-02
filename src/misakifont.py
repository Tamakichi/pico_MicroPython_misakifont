from misakifontdata import misaki_font_data, misaki_font_table, kana_h2z_map
from tma_jp_utl import isHkana, hkana2kana, han2zen, binfind

class MisakiFont:
    FTABLESIZE =   len(misaki_font_table)     # フォントテーブルデータサイズ
    FONT_LEN   =   7                          # 1フォントのバイト数
    FONT_TOFU  =   0x25a1                     # 豆腐"□"コード

    def __init__(self):
        pass

    #  フォントコード検索
    #  引数   ucode UTF-16 コード
    #  戻り値 該当フォントがある場合 フォントコード(0～FTABLESIZE-1)
    #        該当フォントが無い場合 -1
    def find(self, ucode):
        return binfind(ucode, len(misaki_font_table), lambda pos:misaki_font_table[pos] )

    # 半角カナ文字判定
    #  引数   ucode UTF-16 コード
    def isHkana(self, ucode):
        return isHkana(ucode)

    # 半角カナ全角文字変換
    #  引数   ucode UTF-16 コード
    def hkana2kana(self, ucode):
        return hkana2kana(ucode)

    # UTF16半角文字コードをUTF16全角文字コードに変換する
    # (変換できない場合は元のコードを返す)
    #  引数   ucode UTF-16 コード
    #  戻り値: 変換コード
    def han2zen(self, ucode):
        return han2zen(ucode)

    #  UTF16文字コードに対応する美咲フォントデータ8バイトを取得する
    #  引数   ucode UTF-16 コード
    #  戻り値: 正常終了 取得したデータ(トプル) 、異常終了 None
    def font(self,utf16,flgz=True):
        if flgz:
            utf16 = self.han2zen(utf16)
        code  = self.find(utf16)
        if code < 0: # 該当するフォントが存在しない
            code = self.find(self.FONT_TOFU)
        return misaki_font_data[code*self.FONT_LEN:code*self.FONT_LEN+self.FONT_LEN] + (0,) 
