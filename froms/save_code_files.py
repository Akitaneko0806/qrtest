import os

# 指定されたディレクトリのファイルとフォルダを一覧表示する関数
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

# Flaskアプリケーションのディレクトリ
flask_app_directory = '/mnt/data/app'

# ディレクトリとファイルの一覧を表示
list_files(flask_app_directory)
