import time
import Getch as gch
import picamera
getch = gch.Getch()
w = getch() #一文字取得 
while w!='e':
	#camera使用
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768) #解像度設定
        camera.start_preview() #準備
        time.sleep(2) #準備待ち
        imgStream = io.BytesIO() #保存領域作成
        camera.capture(imgStream,format='jpeg') #撮影
        data = np.fromstring(imgStream.getvalue(),dtype=np.uint8) #numpy配列に変換
        image = cv2.imdecode(data,1) #メモリバッファから読み込み
        cv2.imwrite("cap.png",image) #画像保存
        print("capture")
    w=getch()
