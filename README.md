# oreo
このbranchはGoPiGoの環境構築および基本的な動作のサンプルプログラムのbranchである。

forward_2seconds.pyはpython fileであり、2秒間GoPiGoを前進させ、その後停止するプログラムである。

socket_print.pyはpython fileであり、vision systemとsocket通信を行い、受信した座標情報を標準出力するプログラムである。

shutter.pyは'e'以外のキーを押すと撮影,保存するプログラムである。

shutter2.pyは常に判定し続けてマーカーが範囲内に存在すれば自動で撮影し保存するプログラムである。

keyboardControl.pyは'w','s','a','d'でそれぞれ前進,後退,左回転,右回転し,'e'で終了するプログラムである。

shutterGame.pyはshutter.pyとkeyboardControl.pyを組み合わせてさらに採点メソッドを追加したサンプルプログラムである。
