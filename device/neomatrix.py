# NeoPixel ドットマトリックス表示ドライバ
from machine import Pin
from neopixel import NeoPixel
import time

class NeoMatrix:
    width  = 8
    height = 8
    
    # コンストラクタ
    def __init__(self, pin, w=8, h=8):
        self.width = w
        self.height = h        
        self.pin = Pin(pin, Pin.OUT) 
        self.np  = NeoPixel(self.pin, self.width*self.height)

    # ドットマトリックス 指定座標ピクセル番号変換
    def XYtoNo(self, x, y):
        return self.width*y + x if y&1 else self.width*y + self.width-1 -x

    # 表示更新
    def update(self):
        self.np.write()

    # 表示クリア
    def cls(self,flgUpdate=False):
        self.np.fill((0,0,0))
        if flgUpdate:
            self.np.write()

    # 点の描画
    def pixcel(self,x,y,color,flgUpdate=False):
        self.np[self.XYtoNo(x,y)] = color
        if flgUpdate:
            self.np.write()   
 
     # 全領域塗りつぶし
    def fill(self,color,flgUpdate=False):
        self.np.fill(color)
        if flgUpdate:
            self.np.write()

    # 単色8x8ビットマップの配置
    def putBitmap(self, bmp, fg, bg, flgUpdate=False):
        for y in range(0,self.height-1):
            for x in range(0,self.width-1):
                self.np[XYtoNo(x,y)] = fg if (0x80>>x) & bmp[y] else bg
        if flgUpdate:
            self.np.write()

    # ドットマトリックス 左スクロール
    def scroll(self, flgUpdate=False):
        for y in range(self.height):
            for x in range(1,self.width):
                self.np[self.XYtoNo(x-1,y)] = self.np[self.XYtoNo(x,y)]
            self.np[self.XYtoNo(self.width-1,y)]  = [0,0,0]
        if flgUpdate:
            self.np.write()

    # 1文字左スクロール挿入
    def scrollIn(self, fnt, color, tm, ypos=0, fw=8, fh=8):
        for i in range(0,fh):
            self.scroll()
            for j in range(0,fw): # フォントパターン1列分のセット
                self.np[self.XYtoNo(self.width-1,j+ypos)] = color if fnt[j] & (0x80 >> i) else (0, 0, 0)
            self.np.write()
            time.sleep_ms(tm)

    # 直線を引く
    def drawline(self, x0, y0, x1, y1, color, flg=True):    
        dx=abs(x1-x0)
        dy=abs(y1-y0)
        sx=(0 < (x1-x0)) - ((x1-x0) < 0)
        sy=(0 < (y1-y0)) - ((y1-y0) < 0)
        err=dx-dy   
        if (x0!=x1) or (y0!=y1): 
            self.np[self.XYtoNo(x1,y1)] = color

        while True:
            self.np[self.XYtoNo(x0,y0)] = color        
            e2=2*err
            if e2 > -dy:
                err-=dy
                x0+=sx

            if e2 <  dx:
                err+=dx
                y0+=sy
            if not ((x0!=x1) or (y0!=y1)):
                break
        if flg:
            self.np.write()

    # 直線、ボックス、塗りつぶしボックスの描画
    def line(self, x1, y1, x2, y2, color, mode=0, flg=True): 
        if mode == 0:
            # 直線
            self.drawline(x1,y1,x2,y2,color,False)
     
        elif mode == 1:
            # 矩形
            self.drawline(x1,y1,x2,y1,color,False)
            self.drawline(x1,y1,x1,y2,color,False)
            self.drawline(x1,y2,x2,y2,color,False)
            self.drawline(x2,y2,x2,y1,color,False)
        else:
            # 矩形塗りつぶし
            w = abs(x1-x2)
            h = abs(y1-y2)
            x=x2 if x1>=x2 else x1
            y=y2 if y1>=y2 else y1
            for i in range(0,h+1):
                self.drawline(x,y+i,x+w,y+i,color,False)      
        if flg:
            self.np.write()
