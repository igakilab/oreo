import subprocess
import os
import math
import atexit
import threading
import sys
import Sub

IMG_DIR = "/var/www/html/photo/"  # 生成されるファイルのディレクトリ


# ゲーム開始
def main():
    print("main called")

    # ゲーム開始時に採点画像を削除
    index = 1
    while True:
        path = IMG_DIR + "saiten/cap" + str(index) + ".png"
        if (os.path.exists(path)):
            os.remove(path)
            index += 1
        else:
            break
    # 採点結果のテキストファイルを初期化
    f = open("/var/www/html/photo/saiten/kekka.txt", "w")
    f.write("0,0,")
    f.close()

    Sub.setControl(True)  # コントロール可能に
    print("main end")


if __name__ == "__main__":
    Sub.sub()  # Sub起動
    main()  # 起動
