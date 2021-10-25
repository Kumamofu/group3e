# jsonの読み込みとcsvへのデータ書き込み
import json
import pandas as pd
import numpy as np
import glob
import csv


def getFileName(path):
    filelist = sorted(glob.glob(path + "/*"))
    return filelist


def getSpecificData(filelist):
    for i in range(len(filelist)):
        with open(filelist[i]) as f:
            data = json.load(f)
            data = np.array(data['people'][0]
                            ['pose_keypoints_2d']).reshape(-1, 3)
        df = pd.DataFrame(data, columns=['X', 'Y', 'P'], index=["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip",
                                                                "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"])
        """ sample
        # 自分の必要なデータを取り出す
        writeCSV([float(df.at["RElbow", "X"]), float(df.at["RElbow", "Y"]), float(df.at["RWrist", "X"]), float(df.at["RWrist", "Y"]), float(
            df.at["LElbow", "X"]), float(df.at["LElbow", "Y"]), float(df.at["LWrist", "X"]), float(df.at["LWrist", "Y"])])
"""

        # 猫背を判定

        a = np.array([float(df.at["Nose", "X"]),
                      float(df.at["Nose", "Y"])])

        b = np.array([float(df.at["Neck", "X"]),
                      float(df.at["Neck", "Y"])])

        c = np.array([float(df.at["MidHip", "X"]),
                      float(df.at["MidHip", "Y"])])

        vec_a = a-b
        vec_c = c-b

        # コサインの計算
        length_vec_a = np.linalg.norm(vec_a)
        length_vec_c = np.linalg.norm(vec_c)
        inner_product = np.inner(vec_a, vec_c)
        cos = inner_product / (length_vec_a * length_vec_c)

        # 角度（ラジアン）の計算
        rad = np.arccos(cos)
        nekoze = 0
        # 弧度法から度数法（rad ➔ 度）への変換
        degree = np.rad2deg(rad)

        if degree <= 120:
            nekoze = 1

        # 猫背検出に必要なデータのみ取り出す
        writeCSV([i, float(df.at["Nose", "X"]), float(df.at["Nose", "Y"]), float(df.at["Neck", "X"]), float(df.at["Neck", "Y"]), float(
            df.at["MidHip", "X"]), float(df.at["MidHip", "Y"]), degree, nekoze])


def writeCSV(data):
    # CSVへの書き込み
    with open('output.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(data)


def inputJson():
    filelist = getFileName('./sample')
    with open('output.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        print()
        """sample
        # 自分の必要なデータの列の名前を用意。上のデータと同じだけの列数を揃える。
        writer.writerow(["RElbow_x", "RElbow_y", "RWrist_x", "RWrist_y",
                        "LElbow_x", "LElbow_y", "LWrist_x", "LWrist_y"])
                        """

        writer.writerow(
            ["FrameNo", "Nose_x", "Nose_y", "Neck_x", "Neck_y", "MidHip_x", "MidHip_y", "degree", "nekoze"])

    getSpecificData(filelist)


def main():
    inputJson()


if __name__ == '__main__':
    main()
