import os
import sys

# コマンドライン引数が渡されているか確認
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Usage: python rename_images.py <directory_path> <extension> [prefix]")
    sys.exit(1)

# コマンドライン引数からディレクトリパス、拡張子、プレフィックスを取得
directory = sys.argv[1]
extension = sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) == 4 else "image"  # プレフィックスが指定されていない場合はデフォルトで "image"

# ディレクトリが存在するか確認
if not os.path.isdir(directory):
    print(f"Error: The directory {directory} does not exist.")
    sys.exit(1)

# 拡張子が適切か確認（先頭のドットを含むことを確認）
if not extension.startswith('.'):
    print("Error: Extension should start with a dot (e.g. '.jpg').")
    sys.exit(1)

# ディレクトリ内の指定された拡張子のファイルを取得
files = [f for f in os.listdir(directory) if f.endswith(extension)]

# ファイルが見つからない場合の処理
if not files:
    print(f"No {extension} files found in the directory: {directory}")
    sys.exit(1)

# ソートして順番通りにリネーム
for i, file in enumerate(sorted(files), start=1):
    old_name = os.path.join(directory, file)
    new_name = os.path.join(directory, f"{prefix}{i}{extension}")
    os.rename(old_name, new_name)
    print(f"Renaming {file} to {prefix}{i}{extension}")
