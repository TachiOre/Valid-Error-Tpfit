"""描画モジュール
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import axes
from matplotlib import patches
from adjustText import adjust_text

def draw_poly(
    points: list,
    ax: axes.Axes = None,
    **kwargs,
) -> tuple:
    """2-D配列に格納されたポリゴンの頂点情報を基に，ポリゴンをプロットする．

    Args:
        polygon (list): ポリゴンの各頂点を格納した2-D配列
            [[x0,y0],[x1,y1],...,[xn,yn]]
        label (bool): 頂点の番号を表示するかどうか
        ax (axes.Axes, optional): プロットしたいaxを指定.Noneを渡すと新たにfig(matplotlib.figure.Figure)とax(matplotlib.axes.Axes)が作られる． Defaults to None.

    Returns:
        tuple: 描画したmatplotlib.figure.Figureとmatplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    else:
        fig = ax.figure

    draw_x = [p[0] for p in points]
    draw_x.append(draw_x[0])
    draw_y = [p[1] for p in points]
    draw_y.append(draw_y[0])

    l2d = ax.plot(draw_x, draw_y, **kwargs)
    ax.set_aspect("equal")

    return fig, ax

def draw_line(
        ax: axes.Axes = None,
        **kwargs,
    ) -> tuple:
    
    if ax is None:
        fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure 
    
    draw_x = [p[0] for p in points]
    draw_x.append(draw_x[0])
    draw_y = [p[1] for p in points]
    draw_y.append(draw_y[0])

    ax.plot(draw_x, draw_y, **kwargs)

    return fig, ax