"""
便利な関数モジュール
"""
import os
import numpy as np
import math
#作り直し
def remove_same(array_2d: np.ndarray, tol: float = 1e-8):
    """
    二次元の同じ要素があった時、それを削除する関数
    Args:
        array_2d: np.array
        tol: float, 許容誤差
    """
    unique_rows = []
    for row in array_2d:
        is_unique = True
        for unique_row in unique_rows:
            if all(math.isclose(x, y, rel_tol=tol) for x, y in zip(row, unique_row)):
                is_unique = False
                print("same")
                break
        if is_unique:
            unique_rows.append(row)
    return np.array(unique_rows)

def make_folder(output_folder):
    """
    同じディレクトリにフォルダを作成する
    Args:
        output_folder (str):出力したいフォルダ名
    return:
    """
    # https://note.nkmk.me/python-os-mkdir-makedirs/
    try:
        os.mkdir(output_folder)
    except FileExistsError:
        print("output_folder is already exsisted")
        pass

class PolyNPolygon:
    """
    多角形に関する関数モジュール：ポリNポリポリゴン

    """
    def __init__(self, points):
        """
        ポリNポリゴンクラスのコンストラクタ
        Args:
            points(np.array):多角形の点群を表す座標のリスト。各座標はタプル (x, y) で表現されます 
        """
        self.__points = points
    
    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, value):
        if value is None :
            raise ValueError("points cannot be set to None")
        elif not isinstance(value, np.ndarray):
            error_msg=  f"points must be a numpy.ndarray, but got {type(value).__name__}"
            raise ValueError(error_msg)
        self.__points = value
    
    def interpolate_line(self,p1, p2, q1, q2):
        """
        2つの線分 (p1, p2) と (q1, q2) の交点を見つける関数

        Args:
            p1 (np.array): 線分1の始点の座標。
            p2 (np.array): 線分1の終点の座標。
            q1 (np.array): 線分2の始点の座標。
            q2 (np.array): 線分2の終点の座標。

        Returns:
            intersection (np.array): 交点の座標。交点が存在しない場合は None。
        """
        # 線分の傾きが同じ場合、交点は存在しない
        if np.cross(p2 - p1, q2 - q1) == 0:
            return None
        
        t = np.cross(q1 - p1, q2 - q1) / np.cross(p2 - p1, q2 - q1)
        u = np.cross(p2 - p1, q1 - p1) / np.cross(p2 - p1, q2 - q1)
        # 0 <= t <= 1 かつ 0 <= u <= 1 の場合、線分が交差している
        if 0 <= t <= 1 and -1 <= u <= 0:
            intersection = p1 + t * (p2 - p1)
            return intersection
        else:
            return None
    
    def find_intersection_with_line(self, line):
        """
        多角形と直線の交点を見つけるメソッド。

        Args:
            points (np.array): 直線の2点を表す座標のリスト。[(x1, y1), (x2, y2)]

        Returns:
            points_intersection(np.array) :交点の座標のリスト。各座標は np.array([x, y]) です。
        """
        j = 0
        for i in range(len(self.points)):
            
            p1 = np.array(self.points[i])
            p2 = np.array(self.points[(i + 1) % len(self.points)])
            # print(type(p1))
            # print(p2) 
            # print(np.array(line[0]), type(np.array(line[1])) )
            intersection = self.interpolate_line(p1, p2, np.array(line[0]), np.array(line[1]))
            num_on_line=0
            if intersection is not None: 
                for point in intersection:
                    if PolyNPolygon.judge_point_line(point,line) is True:
                        num_on_line = num_on_line+1
                if num_on_line == 1:
                    continue
                if j ==0:
                    points_intersection =intersection[np.newaxis, :]
                    j = 1
                else:
                    points_intersection=np.concatenate([points_intersection,intersection[np.newaxis, :]])
                    # print("before",points_intersection)
                    points_intersection =points_intersection.flatten().reshape(points_intersection.shape[-2], points_intersection.shape[-1] )
                    # print("after",points_intersection[0,1]==points_intersection[-1,1])
                    points_intersection=remove_same(points_intersection)  
                    # print("after",points_intersection)

        return points_intersection
    
    @staticmethod
    def func_extend_from_vec(point,vec_n, mag):
        """
        point (x,y)座標からベクトル方向にmag倍した線分を作成して直線を作る
        
        Args:
            point(np.array)
            vec_n(np.array)
            mag (float)
        
        Retuns:
            line_extend_from_vec(np.array)
        
        """
        return( np.array([point+ vec_n*-mag, point+vec_n*mag]) )
    @staticmethod
    def extend_segment_to_line(line):
            """
            線分を延長して直線にする関数
            Args:
                line(np.array| [ [x,y],[x,y] ]):線分の2点からなる(x,y)座標のリスト
            Return:
                extend_line(np.array) :線分を無限近く延長した直線の(x,y)座標リスト
            """
            center_point = np.mean(line, axis=0)
            vec=np.squeeze(np.diff(line,axis=0))

            return np.array([center_point-vec*99999,center_point+vec*99999])
    
    @property
    def centroid(self):
        return np.mean(self.points, axis=0) #重心位置
    
    @staticmethod
    def rotate_line(line,centroid, angle_deg):
        """
        多角形の重心を中心に直線を指定した角度だけ回転移動させる関数

        Args:
            self.points(np.array)
            centroid(np.array):重心の(x,y)座標
            angle_deg(float):指定した角度[deg]
        
        Retuns:
            line_rotated(np.array):回転した直線
        """
        # 重心を原点に移動
        translated_line = line - centroid

        # 度数法からラジアンに変換
        angle_rad = np.deg2rad(angle_deg)

        # 回転行列を作成
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                    [np.sin(angle_rad), np.cos(angle_rad)]])

        # 直線を回転
        rotated_line = np.dot(rotation_matrix, translated_line.T).T

        # 重心を元に戻す
        line_rotated = rotated_line + centroid

        return line_rotated
    
    @staticmethod
    def split_line_segment(segment, distance):
        """
        指定された距離で線分を分割する関数

        Args:
            segment (ndarray): 分割する線分を表す2つの点の座標を持つnumpy配列。shapeは (2, 2) とします。
            distance (float): 線分を分割する距離

        Returns:
            ndarray: 分割された点の座標を持つnumpy配列。
        """
        # print(segment)
        # 線分の始点と終点を取得
        start_point, end_point = segment
        
        # 線分の長さを計算
        segment_length = np.linalg.norm(end_point - start_point)
        
        # 分割される点の数を計算
        num_divisions = int(np.ceil(segment_length / distance))
        
        # 分割された点の座標を計算
        split_points = []
        for i in range(num_divisions + 1):
            ratio = i / num_divisions
            split_point = start_point + ratio * (end_point - start_point)
            split_points.append(split_point)
        
        return np.array(split_points)

    @staticmethod
    def judge_point_line(point,line):
        u = point - line[0]
        v = line[1] - line[0]

        L = abs(np.cross(u,v)/ np.linalg.norm(u) )
        is_on_line = False
        if L < 0.0001:
            is_on_line =True
        return is_on_line, L
    
    @staticmethod
    def jugde_point_over_line(point, line):

        diff_line = np.squeeze(np.diff(line, axis=0) )
        # print(diff_line)
        inc = diff_line[1]/diff_line[0]
        # print("inc:",inc)
        is_over_line =  point[1] >line[0][1] + inc*(point[0]-line[0][0] )
        # print( is_over_line)
        return is_over_line
        

#ここでエラーsegとverticalの次元が合わない
    def calculate_symmetry_axis_intersection(self,rotated_line,distance_split=1):
        """
            対称軸候補の分割点を通る垂線と多角形の交点を求める関数
        """
        rotated_segment= self.find_intersection_with_line(rotated_line)
        segments =PolyNPolygon.split_line_segment(rotated_segment,distance_split)
        print("total_segments: ",segments.shape[0] )
        segments_modi= None
        vertical_segments= None

        for i,seg in enumerate(segments):
            if i%10 == 0: print(i,"/",segments.shape[0])
            vertical_line = PolyNPolygon.rotate_line(rotated_line,seg,90)
            vertical_segment : np.array =self.find_intersection_with_line(vertical_line)

            # segments_modi =segments_modi.flatten().reshape(segments_modi.shape[-2], segments_modi.shape[-1] )
            # segments_modi=remove_same(segments_modi)  

            if PolyNPolygon.jugde_point_over_line(vertical_segment[0], rotated_line) == PolyNPolygon.jugde_point_over_line(vertical_segment[1], rotated_line): continue
            if vertical_segments is None:
                vertical_segments = vertical_segment
                segments_modi = seg[np.newaxis]
            else:
                # print(vertical_segments.shape)
                # print(segments_modi.shape)
                vertical_segments =vertical_segments.flatten().reshape(vertical_segments.shape[-2], vertical_segments.shape[-1] )
                vertical_segments =np.concatenate( ( vertical_segments, vertical_segment))
                vertical_segments=remove_same(vertical_segments)  

                segments_modi = np.concatenate( ( segments_modi, seg[np.newaxis]))
        if vertical_segments is not None:
            vertical_segments=vertical_segments.reshape(-1,2,2)
        # print()
        # print(vertical_segments.shape)
        # print(segments_modi.shape)

        return segments_modi, vertical_segments



    def calculate_symmetry(self,segments,axis_intersection):
        """
            対称軸から輪郭までの左右の距離の差を求める関数
        """
        # print(axis_intersection.shape)
        # print(type(axis_intersection))
        # print(axis_intersection)
        # if isinstance(axis_intersection[0],np.ndarray):
        #     print("jjj")
        # print(axis_intersection)
        # print()
        # print("segments:", segments)
        # print("axis_intersection :",axis_intersection[:,0,:])
        # if axis_intersection is None:
        #     print("r1: None")
        # else:
        #     print("r1:",axis_intersection.shape)
        # if segments is None: print("r1_segment: None")
        # else: print("r1_segment:",segments.shape)
        r1=segments-axis_intersection[:,0,:]
        r2=axis_intersection[:,1,:]-segments
        diff_distance = np.linalg.norm(r1,axis=1)-np.linalg.norm(r2,axis=1)
        r_distance = np.linalg.norm(r1+r2,axis=1)
        symmetry_score =np.sum(diff_distance**2)

        return symmetry_score,segments,r_distance
    

    def optimize_axis_line(self,center=None,num_split=100):
        """
        重心位置を中心として対称軸を最適化する関数
        Args:
            center(np.ndarray): 最適化するための中心点 dafault:self.centroid
            num_split(int):　対称軸の分割数
        Retruns:
            line_symmetry :最適化された対称軸座標( (x1,y1), (x2,y2))
            data_segments : 刻み幅に従った対称軸座標の分割点群
            data_r :        対称軸の分割点群に対応した輪郭の幅データ
        """
        if center is None: center = self.centroid
        line_init= PolyNPolygon.extend_segment_to_line(np.array([self.points[0], center ]))
        # line_init=self.find_intersection_with_line(line_init)
        line_symmetry=line_init
        # print(line_init)
        segments, axis_intersection=self.calculate_symmetry_axis_intersection(line_init,num_split)
        symmetry_score, data_segments,data_r = self.calculate_symmetry(segments,axis_intersection)
        angle_best = 0
        for angle in range(0,180):
            # print("angel_deg: ",angle)
            line_symmetry_tmp=PolyNPolygon.rotate_line(line_init, center, angle )
            segments_tmp, axis_intersection_tmp =self.calculate_symmetry_axis_intersection(line_symmetry_tmp,num_split)
            # print("axis_inter :",axis_intersection_tmp.reshape(axis_intersection_tmp.shape[0],2,2 )
            axis=[]
            if  axis_intersection_tmp is None: continue #　分割数が少なかったりすると交点がなくなるときがある対処法
            for ax in axis_intersection_tmp:
                axis_intersection_tmp_t=[ax[0], ax[1]]
                axis.append(axis_intersection_tmp_t)
            axis_intersection_tmp=np.array(axis)
            symmetry_score_tmp , data_segments_tmp,data_r_tmp = self.calculate_symmetry(segments_tmp,axis_intersection_tmp)
            
            if symmetry_score_tmp < symmetry_score:
                axis_intersection = axis_intersection_tmp
                symmetry_score = symmetry_score_tmp
                data_segments = data_segments_tmp
                data_r =data_r_tmp

                line_symmetry = line_symmetry_tmp
                angle_best=angle
        print()
        print("best_angle: ", angle_best)
        print()
        return line_symmetry, data_segments, data_r, symmetry_score

    def optimize_horizon_dir(self,num_split=100, num_split_hor=100):
        """
        重心座標を水平方向に動かしながら対称軸を最適化する関数
        Args:
            center(np.ndarray): 最適化するための中心点 dafault:self.centroid
            num_split(int):　対称軸の分割数
        Retruns:
            line_symmetry :最適化された対称軸座標( (x1,y1), (x2,y2))
            data_segments : 刻み幅に従った対称軸座標の分割点群
            data_r :        対称軸の分割点群に対応した輪郭の幅データ
        """
        def divide_x_interval(x_center, y_center, distance, num_intervals):
            """
            Divide the x-interval from the specified center point into the specified number of intervals.

            Args:
            x_center (float): x-coordinate of the center point
            y_center (float): y-coordinate of the center point
            distance (float): total absolute distance to be covered in the x-direction
            num_intervals (int): number of intervals to divide the distance into

            Returns:
            List of tuples containing x-coordinates of the divisions.
            """
            # Calculate the distance for each interval
            interval_distance = distance / (num_intervals - 1)

            # List to store the x-coordinates of the divisions
            x_divisions = []

            # Start from the left-most point
            current_x = x_center - distance / 2

            # Iterate over the number of intervals
            for _ in range(num_intervals):
                x_divisions.append((current_x, y_center))
                current_x += interval_distance

            return np.array(x_divisions)

        center=self.centroid
        # print("ddd")
        print("center_centroid:",center)
        ax, data_segments, data_r, symmetry_score  =self.optimize_axis_line(center,num_split)
        # print("dd")
        # horizon_line=self.calculate_symmetry_axis_intersection(ax,abs(np.max(self.points[0])-np.min(self.points[1])/2 ))[1][1]
        # print("horizon_line",horizon_line)
        # horizon_segs= self.split_line_segment(horizon_line, num_split_hor)
        horizon_segs=divide_x_interval(center[0],center[1],20,4)

        for i,center_opt in enumerate(horizon_segs[1:horizon_segs.shape[0]-1]):
            print("center_opt",center_opt)
            print("horizoxntal_num: ", i)
            data_opt_tmp  =self.optimize_axis_line(center=center_opt,num_split=num_split)
            if data_opt_tmp[3] < symmetry_score:
                ax, data_segments, data_r, symmetry_score = data_opt_tmp
                print("best num_cen changed to : ",i)
        return ax, data_segments, data_r, symmetry_score
            

    #線分用のクラスを後で作るべき

    """
    ここ以下は未実装の関数
    """
    def get_points(self):
        """
        ポリNポリゴンの構成点群を取得するメソッド。

        Returns:
        - 点群を表す座標のリスト。各座標はタプル (x, y) です。
        """
        return self.points

    
    def calculate_total_area(self):
        """
        ポリNポリゴン全体の面積を計算するメソッド。

        Returns:
        - ポリNポリゴン全体の面積。
        """
        total_area = 0
        for polygon in self.points:
            # 各ポリゴンの面積を計算して合計する
            # 面積計算の具体的な実装はポリゴンの種類により異なるため、必要に応じて行う。
            # 例: シューンの公式やヘロンの公式などを使用する。
            # https://en.wikipedia.org/wiki/Shoelace_formula
            # https://en.wikipedia.org/wiki/Heron%27s_formula
            total_area += self.calculate_polygon_area(polygon)
        return total_area

    def calculate_polygon_area(self, polygon):
        """
        ポリゴンの面積を計算するメソッド。

        Parameters:
        - polygon: 面積を計算する対象のポリゴン。点群を表す座標のリストです。

        Returns:
        - ポリゴンの面積。
        """
        # ポリゴンの面積計算の具体的な実装はポリゴンの種類により異なるため、必要に応じて行う。
        # 例: シューンの公式やヘロンの公式などを使用する。
        # https://en.wikipedia.org/wiki/Shoelace_formula
        # https://en.wikipedia.org/wiki/Heron%27s_formula
        pass

def main():
    # サンプルの多角形の点群
    polygon_points = [np.array([0, 0]), np.array([2, 0]), np.array([2, 2]), np.array([0, 2])]   
    # サンプルの直線の2点
    line_points = np.array([np.array([1, -1]), np.array([1, 3])])

    extend_line= PolyNPolygon.extend_segment_to_line(line_points)
    # print(extend_line)
    # PolyNPolygon インスタンスを作成
    polygon = PolyNPolygon(polygon_points)

    # 多角形と直線の交点を求める
    intersections = polygon.find_intersection_with_line(line_points)
    
    # 結果を表示
    print("多角形の点群:", polygon.get_points())
    print("直線の2点:", line_points)
    print("交点:", intersections)


    t=polygon.calculate_symmetry_axis_intersection(extend_line)[1]
    # for i in t:
    #     for j in i:
    #         print(j[0],",",j[1])    
if __name__ == "__main__":
    main()
