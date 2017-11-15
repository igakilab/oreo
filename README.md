#ShutterChance
#環境設定
-python版opencvのインストール 'sudo apt-get install python-opencv'
-pythonのWebフレームワークTornadoをインストール
 -Tornadoのドキュメント 'http://www.tornadoweb.org/en/stable/'
 -インストールコマンド 'sudo pip install tornado'
-pygameのインストール　'sudo apt-get install python-pygame' 
-実行ファイルダウンロート 'git clone -b player https://github.com/igakilab/oreo'

#実行方法
-cloneしたディレクトリに移動後 'sudo python Main.py'

#生成されるファイル
-Sub.pyの'IMG_DIR/saiten/'内に以下のファイルが生成される
 -'cap(インデックス).png' 撮影した写真ファイル、インデックスは1から始まる
 -'kekka.txt' (撮影した枚数,採点結果)を書き込んだファイル
