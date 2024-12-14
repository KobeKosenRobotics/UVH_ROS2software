import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Float32MultiArray

import argparse

# RecursionError: maximum recursion depth exceeded while calling a Python object
# 490回以上の再帰
import sys
import threading

import numpy as np

import cv2


#csv関連
import csv
import pprint

#時間取得
import datetime





sys.setrecursionlimit(1024*6400) #64MB
threading.stack_size(1024*1024)  #2の20乗のstackを確保=メモリの確保

#変更後の再帰関数の実行回数の上限を表示
print(sys.getrecursionlimit())

#電極間の位置指定
electrode_ponint = [[0,1],[1,0],[2,0],[3,1],[3,2],[2,3],[1,3],[0,2]]

#構築画像の下準備
reconstructed_img = np.zeros((4,4))

#csv初期化時間をJSTで表示
csv_name = 'log' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
with open(csv_name, 'w') as f:
    writer = csv.writer(f)
    #writer.writerow(["initialized at " + str(datetime.datetime.now())])



### Methods ###
def MinMaxNormalization(
    x: int,
    min: int,
    max: int
) -> float:
    norm_x = (x - min) / (max - min)
    return norm_x

def imshow(
    img_norm: float,
    name: str = 'UVH'
) -> None:
    img = img_norm
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 800, 800)
    print(img)
    cv2.imshow(name, np.array(img,np.uint8))
    cv2.waitKey(1)

def log_csv(data_array):
    with open(csv_name, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(' ')
            writer.writerow(data_array)
            writer.writerow(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

class UVH(Node):
    def __init__(self):
        super().__init__('UVH')
        self.sub = self.create_subscription(Int32MultiArray, '/UVH_out',self.msg_callback, 10 )
        self.pub = self.create_publisher(Float32MultiArray,'/reconstructed_UVH', 10)
        
        
        
    def msg_callback(self, msg):
        data_list = msg.data
        print(data_list)
        data_array = np.array(data_list).reshape(2,8)
        log_csv(data_array)
        data_array = MinMaxNormalization(data_array, 0, 2048)
        n_2 = 7
        for n, element in enumerate(data_array[0]):
                reconstructed_img[electrode_ponint[n][0]][electrode_ponint[n][1]] = (element * 0.6 + data_array[1][n] )#* 0.2 + data_array[1][n_2] * 0.2) * 255
                n_2 = n
        # reconstructed_msg.size = 4
        # reconstructed_msg.stride = 16
        # reconstructed_msg.size = 4
        # reconstructed_msg.stride = 4

        print(Float32MultiArray(data = reconstructed_img.reshape(1,-1)[0]))
        reconstructed_msg = Float32MultiArray(data = reconstructed_img.reshape(1,-1)[0])

        print(reconstructed_msg.data)

        self.pub.publish(reconstructed_msg)
        imshow(reconstructed_img)


def main():
    rclpy.init()
    while True:
        node = UVH()
        rclpy.spin(node)


if __name__ == '__main__':
    main()
