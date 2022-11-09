from machine import Pin
from neopixel import NeoPixel
import time

class NeoMatrix:
    # コンストラクタ
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT) 
        self.np  = NeoPixel(self.pin, 64)

    # 8x8ドットマトリックス 指定座標ピクセル番号変換
    def XYtoNo(self, x, y):
        if y&1:
            no = 8*y + x
        else:
            no = 8*y + 7 -x
        return no

    def update(self):
        self.np.write()
        
    def cls(self,flgUpdate=False):
        self.np.fill((0,0,0))
        if flgUpdate:
            self.np.write()
    
    def fill(self,color,flgUpdate=False):
        self.np.fill(color)
        if flgUpdate:
            self.np.write()

    # 単色8x8ビットマップの配置
    def putBitmap(self, bmp, fg, bg, flgUpdate=False):
        for y in range(0,7):
            for x in range(0,7):
                if (0x80>>x) & bmp[y]:
                    self.np[XYtoNo(x,y)] = fg
                else:
                    self.np[XYtoNo(x,y)] = bg
        if flgUpdate:
            self.np.write()

    # ドットマトリックス 左スクロール
    def scroll(self, flgUpdate=False):
        for i in range(0,8):
            if i&1: # 奇数列
                for j in range(0,7):
                    self.np[i*8+j]=self.np[i*8+j+1]                
            else:   # 偶数列   
                for j in range(1,8):
                    self.np[i*8+8-j]=self.np[i*8+8-j-1]
        if flgUpdate:
            self.np.write()

    # 1文字左スクロール挿入
    def scrollIn(self, fnt, color, tm):
        for i in range(0,8):
            self.scroll()
            # フォントパターン1列分のセット
            for j in range(0,8):
              if (fnt[j] & (0x80 >> i)):
                 self.np[self.XYtoNo(7,j)] = color
              else:
                 self.np[self.XYtoNo(7,j)] = (0, 0, 0)        
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
            if x1>=x2:
                x=x2
            else:
                x=x1
            if y1>=y2:
                y=y2
            else:
                y=y1
                
            for i in range(0,h+1):
                self.drawline(x,y+i,x+w,y+i,color,False)      
        if flg:
            self.np.write()
