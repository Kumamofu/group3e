# -*- coding: utf-8 -*-

# 参考:ex12_file.py
# Pillow-8.4.0を入れた
import tkinter
import cv2
import sys
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import input


class VideoViewer(tkinter.Frame):
    # コンストラクタ
    def __init__(self, master=None, fname=None):
        super().__init__(master)
        # サイズを決める
        master.geometry('1280x790')

        filepath = 'result.mov'
        master.title(filepath)

        # 自身(tkinter.Frame)をmaster(mainで作ったroot)に配置
        self.master = master
        self.pack()

        # MainPanel を 全体に配置
        self.mainpanel = tkinter.Label(root)
        self.mainpanel.pack(expand=1)

        # ボタンを作る(rootに紐づけし、押された時に起動する関数も指定)
        self.btnplay = tkinter.Button(root, text='play', command=self.play)
        self.btnstop = tkinter.Button(root, text='stop', command=self.stop)
        self.btnreplay = tkinter.Button(
            root, text='replay', command=self.replay)
        self.btnexit = tkinter.Button(root, text='exit', command=self.exit)
        self.btnplay.pack(side="left")
        self.btnstop.pack(side="left")
        self.btnreplay.pack(side="left")
        self.btnexit.pack(side="right")

        # open video stream
        self.cap = cv2.VideoCapture(filepath)
        ret, frame = self.cap.read()
        if ret == 0:
            print("failed to open video")
            exit()

        self.frame_num = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.do_play = True
        # 先頭フレーム
        self.frameidx = 0

 # ボタンが呼び出す関数を作成
 # インスタンス関数として置く
    def play(self):
        self.do_play = True

    def stop(self):
        self.do_play = False

    def replay(self):
        self.frameidx = 0

    def exit(self):
        # 終了
        exit()

    def update_video(self):

        if self.do_play:
            # idx+の値を変更すると再生速度が変わる
            self.frameidx = self.frameidx+5

        if self.frameidx >= self.frame_num:
            self.frameidx = 0

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameidx)
        # maxフレーム数を取得
        max_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        ret, frame = self.cap.read()

        self.master.geometry('1280x790')

        # 動画の解像度をここで設定
        width = 1280
        height = 720
        half_w = int(width/2)
        half_h = int(height/2)
        # 720pで再生
        frame = cv2.resize(frame, (width, height),
                           interpolation=cv2.INTER_LANCZOS4)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frameに対して文字を追加
        cv2.putText(frame, 'frame: '+str(self.frameidx)+'/'+str(int(max_frame)),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=1)

        # 猫背警告

        if self.frameidx in read_nekoze.rows:
            cv2.putText(frame, 'Nekoze!!!!!!!',
                        (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), thickness=3)

        imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.mainpanel.imgtk = imgtk
        self.mainpanel.configure(image=imgtk)

        # 1ms後に自分自身を呼ぶ
        self.mainpanel.after(1, self.update_video)


if __name__ == "__main__":
    input.inputJson()
    import read_nekoze
    root = tkinter.Tk()
    dig = VideoViewer(master=root, fname="result.mov")
    dig.update_video()
    dig.mainloop()
