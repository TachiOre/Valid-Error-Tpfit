import os
import re

def separate_stepblock(data_txt, key='----------------------------------------------------------------------'):
    lines = data_txt.split(key)
    list_preset= []
    list_isteprow=[]
    for i,block in enumerate(lines) :
        if i ==0:
            line_preset= block.split("\n")
            list_preset.append(line_preset)
        else:
            line = block.split("\n")
            list_isteprow.append(line[1:-1])

    return list_preset, list_isteprow    

def convert_to_figure(value_str):
    if '.' in value_str:
        if 'E' not in value_str:
            if  '+' in value_str:
                figures_splited = value_str.split('+')
                return float(figures_splited[0]+'E+'+figures_splited[1])
            elif '-' in value_str:
                figures_splited = value_str.split('-')
                return float(figures_splited[0]+'E-'+figures_splited[1])
            else:
                return float(value_str)
        else:
            return float(value_str)
    elif 'E' in value_str:
        return float(value_str)
    else:
        return int(value_str)
    


def extract_values(lines, variable_name):
    """
    出力msファイルの記述からパラメータに対応する数値を抽出する。
    
    Args:
        lines: 抽出したい数値が含まれる出力ブロック
        variable_name: 抽出するパラメータ
    Returns:
        values : 抽出するパラメータの数値
    """
    value=None
    for line in lines:
        if variable_name in line:
            parts = re.split('[ =, ]+',line)

            for i in range(len(parts)):
                if parts[i] == variable_name:
                    try:
                        # 等号がある場合を考慮
                        if parts[i + 1] == '=':
                            value_str = parts[i + 2]
                        else:
                            value_str = parts[i + 1]
                        
                        # 数字部分がintかfloatかをチェックして変換
                        # print(value_str)
                        # value = int(value_str) if '.' not in value_str and 'e' not in value_str.lower() else float(value_str)
                        value = convert_to_figure(value_str)
                        # print(value)
                        return value
                        
                    except (IndexError, ValueError):
                        value = None
    
    return value



def extract_values_with_posi(lines, variable_name,is_from_zero=False):
    """
    出力msファイルの記述からパラメータに対応する数値を抽出する。
    
    Args:
        lines: 抽出したい数値が含まれる出力ブロック
        variable_name: 抽出するパラメータ
    Returns:
        values : 抽出するパラメータの数値
    """
    # print(variable_name)
    posi = []
    value=None
    posi_para= None
    for line in lines:
        if variable_name in line:
            parts = re.split('[ =,() ]+',line)
            # print(parts)

            for i in range(len(parts)):
                if parts[i] == variable_name:
                    try:
                        # 等号がある場合を考慮
                        if parts[i + 1] == '=':
                            value_str = parts[i + 2]
                        else:
                            value_str = parts[i + 1]

                        # 該当する点のposiを抽出
                        if is_from_zero is True:

                            posi_para = (convert_to_figure(parts[i+3]),
                                        convert_to_figure(parts[i+4]),
                                        convert_to_figure(parts[i+5])
                                        )
                        else:          
                            posi_para = (convert_to_figure(parts[i+3])-1,
                                        convert_to_figure(parts[i+4])-1,
                                        convert_to_figure(parts[i+5])-1
                                        )



                        # 数字部分がintかfloatかをチェックして変換
                        value = convert_to_figure(value_str)
                        return value,posi_para
                    
                    except (IndexError, ValueError):
                        value = None
                        posi_para= None
    return value,posi_para