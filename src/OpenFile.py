"""
フォルダー操作に関するモジュール
"""
import os
import shutil
import re
import struct

def make_folder(folder_name, dir_file=None):
    """
    フォルダーを作成する関数
    Args:
        folder_name: 作成するフォルダの名前
        dir_file: フォルダを作成するディレクトリのパス（デフォルトはカレントディレクトリ）
    Returns:
        new_folder_path:作成したフォルダーのパス
    """
    if dir_file is None:
        dir_file = "."

    # ディレクトリが存在しない場合、エラーメッセージを出力して終了
    if not os.path.exists(dir_file):
        print(f"Error: Directory '{dir_file}' does not exist.")
        return
    
    # 作成するフォルダのパスを結合
    new_folder_path = os.path.join(dir_file, folder_name)
    
    # すでに同じ名前のフォルダが存在するかどうかをチェック
    if os.path.exists(new_folder_path):
        print(f"Folder '{folder_name}' already exists in '{dir_file}'.")
    else:
        # フォルダを作成
        os.mkdir(new_folder_path)
        print(f"Folder '{folder_name}' created successfully in '{dir_file}'.")
    return new_folder_path


def copy_rename_file(source_file, dest_folder, new_name):
    """
    ファイルをコピーして指定のフォルダーにペーストする関数
    Args:
        source_file: コピーして名前を変更するファイルのパス
        dest_folder: コピーしたファイルを保存するフォルダのパス
        new_name: 新しいファイル名
    Returns: 
        dst_file: コピーしたファイルのpath
    """
    # ファイルが存在しない場合、エラーメッセージを出力して終了
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' does not exist.")
        return
    
    # ディレクトリが存在しない場合、エラーメッセージを出力して終了
    if not os.path.exists(dest_folder):
        print(f"Error: Destination folder '{dest_folder}' does not exist.")
        return
    
    # ファイルのベース名と拡張子を取得
    base_name, extension = os.path.splitext(os.path.basename(source_file))
    
    # コピーして名前を変更したファイルのパス
    dest_file = os.path.join(dest_folder, new_name + extension)
    
    # ファイルをコピーして名前を変更して保存
    shutil.copyfile(source_file, dest_file)
    
    print(f"File copied and renamed successfully to '{dest_file}'.")
    return dest_file

def get_shared_name(data_path, extension=""):
    file_names=[]
    items = []
    # 指定したディレクトリ内の直下にあるファイルを取得します
    for item in os.listdir(data_path):
        item_path = os.path.join(data_path, item)

        if os.path.isfile(item_path):
            file_name, file_extension = os.path.splitext(item)
            # ファイル名から前半部分を抽出し、共通する部分を取得します
            if file_extension == extension:
                file_names.append(file_name)
                items.append(item)
    if len(items)==0:
        print("該当する拡張子のファイルはありません")
    common_prefix = os.path.commonprefix(file_names)

    return common_prefix,items



def get_numbered_files(folder, extension):
    """
    指定した拡張子のファイル名群を取得する関数
    Args:
        folder: フォルダのパス
        extension: 拡張子（例: '.txt', '.jpg'）
    Returns:
        lst: 指定した拡張子のファイル名群
    """
    numbered_files = []

    # フォルダ内のファイルを走査
    for file_name in os.listdir(folder):
        # 拡張子が一致するかを確認
        if file_name.endswith(extension):
            # ファイル名の連番部分を正規表現で検索
            match = re.match(r'(.+?)(\d+)(\..+)', file_name)
            if match:
                numbered_files.append(file_name)
                
    # ファイル名の連番の部分でソート（数値の大小でソート）
    numbered_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    def _swap_first_and_second(lst):
        if len(lst) >= 2:
            print("0番目:",lst[0])
            print("1番目:",lst[1])
            # lst[0], lst[1] = lst[1], lst[0]
        return lst
    # numbered_files=_swap_first_and_second(numbered_files)
    numbered_files = _swap_first_and_second(numbered_files)        
    return numbered_files

def copy_remove_same(path_original,path_new_folder):
    """
    Args: 
        path_original:コピー元となるリスト群が含まれるフォルダーパス
        path_new_folder: ペーストするフォルダ
    Returns:
        list_path_copy_file
    """
    list_path_copy_file=[]
    list_numbered_files = get_numbered_files( path_original, ".txt")
    for i,p  in enumerate(list_numbered_files):
        base_name, _ = os.path.splitext(os.path.basename(p))
        path_copy_file=copy_rename_file(os.path.join(path_original, p), path_new_folder, base_name )
        list_path_copy_file.append(path_copy_file)
        with open(path_copy_file) as f:
            s = f.read()
            list_s = s.splitlines() 
            list_s_rem = list(set(list_s))
        with open(path_copy_file,"w", encoding="utf-8") as f:
            for s in list_s_rem:
                f.write(s)
                f.write('\n')
        # if(i==0):
        #     break
    return list_path_copy_file

def get_data_from_binary(filename):
    """
    バイナリデータを単精度浮遊小数点(float)として読み込む
    """

    #ファイル読み込み
    with open(filename, 'rb') as file:
        # バイナリデータを読み取り
        binary_data_S = file.read()

    # 単精度浮動小数点数に変換
    float_list_S = struct.unpack('f' * (len(binary_data_S) // 4), binary_data_S)
    return float_list_S


def main():
    folder_path = "."
    extension = ".txt"
    new_folder_name=["train", "val"]
    ratio_train=0.7

    original_name=get_numbered_files(folder_path,extension) 
    total_img=len(original_name)
    num_img=[int(total_img*ratio_train),total_img]

    print(num_img)

    for name in new_folder_name:
        make_folder(name)
    for i,p in enumerate(original_name):
        if i <  num_img[0]: copy_rename_file( folder_path+"/"+p ,folder_path+"/"+new_folder_name[0] , new_folder_name[0] +str(i) )
        if num_img[0]<= i  <num_img[1] : copy_rename_file( folder_path+"/"+p ,folder_path+"/"+new_folder_name[1] , new_folder_name[1] +str(i) )

if __name__=="__main__":
    main()




# for i,p in enumerate(get_numbered_files(folder_path,extension) ):
#     if i < start_num: continue
#     if i >= end_num : break
#     copy_rename_file( folder_path+"/"+p ,folder_path+"/"+new_folder_name , new_folder_name+str(i) )
        
    # break

# for file_name in os.listdir(folder_path):
#     print(file_name)