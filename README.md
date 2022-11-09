# pico_MicroPython_misakifont
Raspberry Pi Pico MicroPython用美咲フォント利用モジュール

## 概要

Raspberry Pi Pico MicroPython用の美咲フォントドライバライブラリです。  
フラッシュメモリ消費を抑えるため、フォントを  
教育漢字1,006字(小学校で習う漢字）＋ひらがな・カタカナ・記号・半角等の1,710字に絞っています。  

※ 美咲フォントは、Little Limitさんが開発し、配布しているフォントです。  
   8×8 ドット日本語フォント「美咲フォント」  
   <http://littlelimit.net/misaki.htm>

収録文字  
![対応フォント](img/教育漢字.PNG)

## 仕様

* 文字コード  UTF16/UTF-8  
* フォントサイズ  8x8ドッド（美咲フォント)  
* フォント格納形式  
![format](img/fontFormat.png)

* 利用可能フォント数  1,710字（Arduinoのフラッシュメモリ上に格納）  
  * 漢字 教育漢字 1,006字(小学校で習う漢字）  
  * 非漢字 全角 546字(全角英数字、ひらがな、かたかな、記号)  
  * 半角フォント  158字(半角記号、半角英数、半角カタカナ）  

## 配布ファイル
* /src  
  * misakifont.py　　　　　　　　　美咲フォントクラスモジュール  
  * misakifontdata.py　　　　　　　美咲フォントデータ  
  * sample_misaki.py　　　　　　　 サンプル1（コンソール上にフォントデータを表示）  
  * sample_misaki_neopixel.py　　　サンプル2（8x8ドットNeopixcelにフォント表示）  
  * neomatrix.py　　　　　　　　　 サンプル2用 NeoPixcel利用モジュール  
* README.txt  
* /img  
