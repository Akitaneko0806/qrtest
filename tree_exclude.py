import os

def list_directory_tree(root_dir, exclude_dirs=None, indent=''):
    if exclude_dirs is None:
        exclude_dirs = []

    items = os.listdir(root_dir)
    for item in items:
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            if item not in exclude_dirs:
                print(f"{indent}├── {item}/")
                list_directory_tree(item_path, exclude_dirs, indent + '│   ')
        else:
            print(f"{indent}├── {item}")

def main():
    root_dir = "C:\\Users\\2880\\Desktop\\forms\\froms"  # ディレクトリのパスを変更してください
    exclude_dirs = ['venv', 'logs','__pycache__','pytest_cache','instance','output_files','tests',]
    print(root_dir)
    list_directory_tree(root_dir, exclude_dirs)

if __name__ == '__main__':
    main()
