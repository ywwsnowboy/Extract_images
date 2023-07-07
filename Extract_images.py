import os
import re
import requests
import shutil


def download_images(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r"!\[.*\]\((.+)\)", content)
        for url in matches:
            if url.startswith("http") or url.startswith("https"):
                asset_path = os.path.join(
                    os.path.dirname(path), 'assets', os.path.basename(url))
                if not os.path.exists(os.path.dirname(asset_path)):
                    os.makedirs(os.path.dirname(asset_path))
                if not os.path.exists(asset_path):
                    with requests.get(url, stream=True) as r, open(asset_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                content = content.replace(
                    url, f"./assets/{os.path.basename(url)}")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


def batch_download_images(rootpath):
    for subdir, _, files in os.walk(rootpath):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(subdir, file)
                download_images(path)
                print(f"Images in {path} have been downloaded.")


# 定义旧文件夹和新文件夹
old_dir = './old'
new_dir = './new'
delete_file_in_new = 'README.md'

# 检查文件夹是否存在
if os.path.exists(new_dir):
    # 删除文件夹及其内容
    shutil.rmtree(new_dir)
    os.makedirs(new_dir)
else:
    os.makedirs(new_dir)

shutil.copytree(old_dir, new_dir, dirs_exist_ok=True)
batch_download_images(new_dir)

# 删除不需要转换的README.md文件
file_path = os.path.join(new_dir, delete_file_in_new)
if os.path.exists(file_path):
    os.remove(file_path)
print("all images was extract successfully in new/assets/ directory！")





