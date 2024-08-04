import numpy as np

class Point:
    """
    xy座標内の点に関するクラス
    """
    def __init__(self, point:np.ndarray = None ,is_mm:bool = False):
        """
        ポイントクラスのコンストラクタ
        Args:
            point(np.ndarray) :点のx,y座標
            is_mm( bool) : 点がmmスケールの単位になっているか（なっていない場合,Falseでpxスケール)
        """
        self.__point = point
        self.is_mm = is_mm
        
    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        if value is None:
            raise ValueError("points cannot be set to None")
    
    def convert_px_to_mm(self, scale):
        """
        スケールをpxからmmスケールに変換する関数
        
        Args:
            self.point : 点の座標(x,y)
            scale : スケール mm/px
        
        """
        if self.is_mm is False:
            # print(self.point*scale)
            self.__point =self.point*scale
            self.is_mm = True
        else:
            print("Already Converted to mm.")
        
class Line:
    """
    線分に関するクラス
    """
    def __init__(self, list_points:[Point], is_mm:bool = False ):
        self.__line = list_points
        self.__is_mm = is_mm
    @property
    def line(self):
        return self.__line
    @line.setter
    def line(self, value:[Point]):
        if value is None or value.shape !=2:
            raise ValueError("line's data is wrong")
        if type(value) is not Point:
            raise ValueError("line is composed of datas <class Point>")
    
    def array_line(self):
        return np.array([p.point for p in self.line])
    
    def find_midpoint(self):
        """
        線分の中点を求める関数
        """
        return Point( np.average(self.array_line(),axis=0 ) )
    
    def calculate_distance(self):
        """
        二点間の距離を求める関数
        
        Returns:
            distance:float : 二点から算出した距離
        """
        return np.linalg.norm( self.line[0].point-self.line[1].point )
    
    
    def convert_px_to_mm(self, scale):
        """
        スケールをpxからmmスケールに変換する関数
        
        Args:
            self.line : 点の座標(x,y)
            scale : スケール mm/px
        
        """
        for pq in self.line:
            pq.convert_px_to_mm(scale)
        self.__is_mm=True

    @property
    def is_mm(self):
        for pq in self.line:
            if pq.is_mm is False:
                self.__is_mm=False
                return self.__is_mm
        self.__is_mm=True
        return self.__is_mm
    # @is_mm.setter
    # def is_mm(self):
    #     for pq in self.line:
    #         if pq.is_mm is False:
    #             self.is_mm=False
    #             return self.is_mm
    #     self.is_mm=True
    #     return self.is_mm
    



class DirectionaRectangle(Line):
    """
    方向性のある長方形に関するクラス
    """
    def __init__(self, list_lines: [Line] = None) -> None:
        self.__lines= list_lines
    @property
    def lines(self):
        return self.__lines
    # @lines.setter
    # def lines(self, value:np.ndarray):