from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d
import numpy as np
import re

def interpolate_grid(x, y, z, u, new_dx):

    interp = RegularGridInterpolator((x, y, z), u) # method = "linear"
    xg,yg,zg=np.meshgrid(x,y,z,indexing='ij')
    new_shape = (int((xg[-1, 0, 0] - xg[0, 0, 0]) / new_dx) + 1,
                 int((yg[0, -1, 0] - yg[0, 0, 0]) / new_dx) + 1,
                 int((zg[0, 0, -1] - zg[0, 0, 0]) / new_dx) + 1)

    new_x, new_y, new_z = np.meshgrid(np.linspace(xg[0, 0, 0], xg[-1, 0, 0], new_shape[0]),
                                       np.linspace(yg[0, 0, 0], yg[0, -1, 0], new_shape[1]),
                                       np.linspace(zg[0, 0, 0], zg[0, 0, -1], new_shape[2]), indexing='ij')

    data2=interp((new_x,new_y,new_z))
    return new_x, new_y, new_z, data2


def read_grid_from_bi(data_path,shared_name):
    #座標データ抽出
    points = []
    for d in ["X","Y","Z"]:

        data_path_ndim=f"{data_path}/{shared_name}{d}_00000"
        #ファイル読み込み
        with open(data_path_ndim, 'rb') as file:
            # バイナリデータを読み取り
            binary_data_ndim = file.read()
    
        # バイナリデータを文字列に変換（適切なエンコーディングを指定）
        text_data = binary_data_ndim.decode('utf-8')  # 例としてUTF-8を使用

        # 正規表現を使って「X-Axis Coordinate」に関連するデータを抽出
        pattern_d= re.compile(r'{}-Axis Coordinate\n([\s\S]*?)(?=\n[A-Z]|$)'.format(d))
        match_d = pattern_d.search(text_data)
        if match_d:
            coordinates = match_d.group(1).strip().split()
            # 数値を浮動小数点数に変換
            coordinates = np.array([float(coord) for coord in coordinates] )
            points.append(coordinates)
    
    return points