# ShutterChance
## セットアップ
### GoPiGo
#### 環境設定
- python版opencvのインストール 
  - [opencv-pythonのドキュメント](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/index.html)
  - インストールコマンド 'sudo apt-get install python-opencv'
- pythonのWebフレームワークTornadoをインストール
  - [Tornadoのドキュメント](http://www.tornadoweb.org/en/stable/)  
  - インストールコマンド 'sudo pip install tornado'
- pygameのインストール
  - [pygameのドキュメント](http://westplain.sakuraweb.com/translate/pygame/)
  - インストールコマンド 'sudo apt-get install python-pygame' 
- 実行ファイルダウンロート 'git clone -b player https://github.com/igakilab/oreo'
- IPアドレス設定
  - Main.pyの46行目のIPアドレスを利用するPC側のIPアドレスに変更
  - index.htmlの10行目のIPアドレスをgopigoのIPアドレスに変更
 
#### 実行方法
- cloneしたディレクトリに移動後 'sudo python Main.py'

#### 生成されるファイル
- Sub.pyの'IMG_DIR/saiten/'内に以下のファイルが生成される
 - 'cap(インデックス).png' 撮影した写真ファイル、インデックスは1から始まる
 - 'kekka.txt' (撮影した枚数,採点結果)を書き込んだファイル

#### ドキュメント
##### [gopigo3 ドキュメント](http://gopigo3.readthedocs.io/en/master/index.html)
  - [easygopigo3　リファレンス](http://gopigo3.readthedocs.io/en/master/api-basic.html#easygopigo3)
##### [picamera ドキュメント](http://picamera.readthedocs.io/en/release-1.13/)
  - [picamera WebSocketStreaming](http://ami-gs.hatenablog.com/entry/2014/04/09/230224)
  - [picamera 画像処理](http://blog.livedoor.jp/tmako123-programming/archives/41536599.html)
  
### PC
#### 環境設定
- javaフォルダ以下をintellijもしくはeclipseのsrcフォルダにコピー 

#### 実行方法
- MainFrame.javaを実行

## 運用
- ゲーム準備
  - 最初にPC側を起動させておき,接続待ちのボタンをクリックし、次にgopigo側のプログラムを起動する。
- ゲームの流れ
  - ゲーム開始までは自由に移動、撮影することが可能
  - PC側でボタンを押すとゲーム開始、カウントが始まる。
  - 時間が無くなればゲーム終了、PC側でブラウザが開き採点結果が表示される。
