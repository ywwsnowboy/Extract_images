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
                asset_path = os.path.join(os.path.dirname(path), 'assets', os.path.basename(url))
                if not os.path.exists(os.path.dirname(asset_path)):
                    os.makedirs(os.path.dirname(asset_path))
                if not os.path.exists(asset_path):
                    with requests.get(url, stream=True) as r, open(asset_path, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                content = content.replace(url, f"./assets/{os.path.basename(url)}")
            # else:
            #     asset_path = os.path.join(os.path.dirname(path), url)
            #     if not os.path.exists(os.path.dirname(asset_path)):
            #         os.makedirs(os.path.dirname(asset_path))
            #     shutil.copyfile(url, asset_path)
            #     content = content.replace(url, f"./{os.path.basename(url)}")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


def batch_download_images(root):
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(subdir, file)
                download_images(path)
                print(f"Images in {path} have been downloaded.")


# 定义旧文件夹和新文件夹
old_dir = './old'
new_dir = './new'


if not os.path.exists(new_dir):
    os.makedirs(new_dir)

shutil.copytree(old_dir, new_dir, dirs_exist_ok=True)

batch_download_images('./new/')










