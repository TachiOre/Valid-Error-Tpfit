
def extract_values(lines, variable_name):
    """
    出力msファイルの記述からパラメータに対応する数値を抽出する。
    
    Args:
        lines: 抽出したい数値が含まれる出力ブロック
        variable_name: 抽出するパラメータ
    Returns:
        values : 抽出するパラメータの数値
    """
    values = []
    for line in lines:
        if variable_name in line:
            parts = line.split()
            for i in range(len(parts)):
                if parts[i] == variable_name:
                    try:
                        # 等号がある場合を考慮
                        if parts[i + 1] == '=':
                            value_str = parts[i + 2]
                        else:
                            value_str = parts[i + 1]
                        
                        # 数字部分がintかfloatかをチェックして変換
                        value = int(value_str) if '.' not in value_str and 'e' not in value_str.lower() else float(value_str)
                        values.append(value)
                    except (IndexError, ValueError):
                        values.append(None)
    return values