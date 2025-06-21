import os
import re
import shutil
import requests

def download_images(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

        # 用于记录已下载的URL和对应的本地路径
        downloaded_urls = {}

        # 处理Markdown格式的图片: ![...](url)
        md_pattern = r"!\[.*?\]\((.+?)\)"
        md_matches = re.findall(md_pattern, content)
        for url in md_matches:
            if url.startswith(("http://", "https://")):
                # 如果已经下载过，直接使用已下载的路径
                if url in downloaded_urls:
                    new_url = downloaded_urls[url]
                else:
                    filename = os.path.basename(url)
                    asset_path = os.path.join(os.path.dirname(path), 'assets', filename)

                    # 确保assets目录存在
                    os.makedirs(os.path.dirname(asset_path), exist_ok=True)

                    # 下载图片
                    if not os.path.exists(asset_path):
                        try:
                            response = requests.get(url, stream=True)
                            if response.status_code == 200:
                                with open(asset_path, 'wb') as img_file:
                                    shutil.copyfileobj(response.raw, img_file)
                            else:
                                print(f"Failed to download {url}, status code: {response.status_code}")
                                continue
                        except Exception as e:
                            print(f"Error downloading {url}: {str(e)}")
                            continue

                    new_url = f"./assets/{filename}"
                    downloaded_urls[url] = new_url

                # 替换内容中的URL
                content = content.replace(url, new_url)

        # 处理HTML格式的图片: <img src="url">
        html_pattern = r'<img\s+[^>]*src\s*=\s*["\'](.*?)["\'][^>]*>'
        html_matches = re.findall(html_pattern, content)
        for url in html_matches:
            if url.startswith(("http://", "https://")):
                # 如果已经下载过，直接使用已下载的路径
                if url in downloaded_urls:
                    new_url = downloaded_urls[url]
                else:
                    filename = os.path.basename(url)
                    asset_path = os.path.join(os.path.dirname(path), 'assets', filename)

                    # 确保assets目录存在
                    os.makedirs(os.path.dirname(asset_path), exist_ok=True)

                    # 下载图片
                    if not os.path.exists(asset_path):
                        try:
                            response = requests.get(url, stream=True)
                            if response.status_code == 200:
                                with open(asset_path, 'wb') as img_file:
                                    shutil.copyfileobj(response.raw, img_file)
                            else:
                                print(f"Failed to download {url}, status code: {response.status_code}")
                                continue
                        except Exception as e:
                            print(f"Error downloading {url}: {str(e)}")
                            continue

                    new_url = f"./assets/{filename}"
                    downloaded_urls[url] = new_url

                # 替换内容中的URL（保持原HTML标签结构）
                content = re.sub(
                    r'(<img\s+[^>]*src\s*=\s*["\'])(' + re.escape(url) + r')(["\'][^>]*>)',
                    r'\1' + new_url + r'\3',
                    content
                )

        # 保存修改后的内容
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
print("All images were extracted successfully to new/assets/ directory!")