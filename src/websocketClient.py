import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
from angleCalculator import AngleCalculator
import config
import cv2
import datetime
import os

class WebsocketClient():

    def __init__(self, host_addr):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)
        self.angleCalculator = AngleCalculator(config.Y0,config.Y1,config.SEARCH_WIDTH)
        # WebSocketAppクラスを生成
        # 関数登録のために、ラムダ式を使用
        self.ws = websocket.WebSocketApp(host_addr,
            on_message = lambda ws, msg: self.on_message(ws, msg),
            on_error   = lambda ws, msg: self.on_error(ws, msg),
            on_close   = lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)

        self.last_update_time = 0

    # メッセージ受信に呼ばれる関数
    def on_message(self, ws, message):
        print("receive : {}".format(message))

    # エラー時に呼ばれる関数
    def on_error(self, ws, error):
        print(error)

    # サーバーから切断時に呼ばれる関数
    def on_close(self, ws):
        print("### closed ###")

    # サーバーから接続時に呼ばれる関数
    def on_open(self, ws):
        while True:
            # print("f")
            update_time = os.stat(config.IMAGE_PATH).st_mtime_ns
            # print("k")
            if update_time <= self.last_update_time:
                # print("m")
                continue
            print("b")
            self.last_update_time = update_time
            time.sleep(2)
            img = cv2.imread(config.IMAGE_PATH)
            self.angleCalculator.set_image(img)
            angle = self.angleCalculator.get_angle()
            if angle > 90:
                angle = 90
            elif angle < -90:
                angle = 90
            self.ws.send("e "+str(int(round(angle,0))))
            # thread.start_new_thread(self.run, ())



    # サーバーから接続時にスレッドで起動する関数
    def run(self, *args):
        while True:
        # for i in range(10):
            time.sleep(0)
            # input_data = input("send data:")
            # img = cv2.imread(config.IMAGE_PATH)
            # self.angleCalculator.set_image(img)
            # angle = self.angleCalculator.get_angle()
            # if angle > 90:
            #     angle = 90
            # elif angle < -90:
            #     angle = 90
            # print(int(angle))
            # print("----------------------------")
            # # self.ws.send("send data:" + "e "+str(int(round(angle,2))))
            # self.ws.send("e "+str(int(round(angle,0))))
        self.ws.close()
        print("thread terminating...")
    
    # websocketクライアント起動
    def run_forever(self):
        self.ws.run_forever()
