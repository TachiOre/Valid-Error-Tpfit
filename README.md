# Vlid-Error-Tpfit
- msファイルから解析の進捗状況を可視化するプログラム


# 環境
Python 3.11
モジュール requirements.txtに記載

# セットアップ
```
py -m venv venv
.\venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
```

その後jupyter notebookのカーネルとしてvenvを選択

# requirements.txtの更新
```
pip freeze --exclude src > requirements.txt
```