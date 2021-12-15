import cv2
import matplotlib.pyplot as plt
import math
import numpy as np

class AngleCalculator():
    def __init__(self,y0,y1,search_width):
        self.y0 = y0
        self.y1 = y1
        self.search_width = search_width
        self.image = None
        self.image_size = None
        self.rgb_array = None 
        self.image_trans = None
        self.image_bianry = None

    def set_image(self, image):
        self.image = image
        self.image_size  = (image.shape[1], image.shape[0])

    # 二値化する
    def _change_to_binary(self):
        gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY) # グレースケール化
        th, self.image_binary = cv2.threshold(gray, 85, 255, cv2.THRESH_OTSU)
        return self.image_bianry

    # 上からみる関数(引数:画像のパス)
    def _up(self):
         # 変換前後の対応点を設定
        p_original = np.float32([[400,200], [808,220], [-1000, 1478], [1108, 1778]])
        p_trans = np.float32([[0,0], [1108,0], [0,1778], [1108,1778]])
         # 変換マトリクスと射影変換
        M = cv2.getPerspectiveTransform(p_original, p_trans)
        self.image_trans = cv2.warpPerspective(self.image_binary, M, self.image_size)
        return self.image_trans

    def _get_lines_mid_point(self, y):
        # rows = self.image_trans[y,:,0]
        rows = self.rgb_array[y,:,0]
        w = self.image_trans.shape[1]
        phase = 0
        x1 = 0
        x0 = 0
        for i in range(w-self.search_width):
            row = rows[i:i+self.search_width]
            if phase == 0 and all(row) :
                phase = 1
            elif phase == 1 and not all(row):
                x0 = i+self.search_width-1
                phase = 2
            elif  phase == 2 and all(row):
                x1 = i
                break
        return ((x0 + x1)/2, y)

    # 角度求める(引数：奥の中点、手前の中点)
    def _calculate_angle(self,p0,p1):
        #3点目は手前の中点から垂直に伸ばした点
        x0, y0 = p0
        x1, y1 = p1
        l = math.sqrt((x0-x1)**2 + (y0-y1)**2)
        h = y1 - y0
        theta = math.acos(h/l)
        angle = theta * (180 / math.pi)
        if x0<x1:
            # print("--")
            angle = -1*angle
        return angle


    # rgbの色配列を返す関数(引数:画像のパス)
    def _get_rgb(self):
        img_gray = cv2.cvtColor(self.image_trans, cv2.COLOR_BGR2RGB) #色配置の変換 BGR→RGB
        self.rgb_array = np.asarray(img_gray)   #numpyで扱える配列をつくる
        # cv2.imwrite("GetAngle/output/rgb_Image.png",img_gray)
        # print(img_array.shape)
        return self.rgb_array

    def get_angle(self):
        assert self.image is not None, "set image first."
        self._change_to_binary()
        self._up()
        self._get_rgb()
        p0 = self._get_lines_mid_point(self.y0)
        p1 = self._get_lines_mid_point(self.y1)
        angle = self._calculate_angle(p0, p1)
        print(str(round(angle,2)))
        return angle
