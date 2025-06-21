import os
import shutil
import re

def process_md_files():
    # 创建new文件夹
    os.makedirs('new', exist_ok=True)

    # 复制所有md文件和attachments文件夹到new目录
    for root, dirs, files in os.walk('old'):
        # 在new中创建对应的子目录
        rel_path = os.path.relpath(root, 'old')
        new_root = os.path.join('new', rel_path)
        os.makedirs(new_root, exist_ok=True)

        # 复制md文件
        for file in files:
            if file.endswith('.md'):
                src = os.path.join(root, file)
                dst = os.path.join(new_root, file)
                shutil.copy2(src, dst)

        # 复制attachments文件夹
        if 'attachments' in dirs:
            src_attachments = os.path.join(root, 'attachments')
            dst_attachments = os.path.join(new_root, 'attachments')
            if os.path.exists(dst_attachments):
                shutil.rmtree(dst_attachments)
            shutil.copytree(src_attachments, dst_attachments)

    # 第一步：转换图片引用格式 ![[...]] -> ![...](...)
    for root, dirs, files in os.walk('new'):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 替换 ![[attachments/xxx]] 为 ![](attachments/xxx)
                new_content = re.sub(
                    r'!\[\[attachments/([^\]]+)\]\]',
                    r'![](attachments/\1)',
                    content
                )
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

    # 第二步：重命名所有attachments文件夹为assets
    for root, dirs, files in os.walk('new'):
        if 'attachments' in dirs:
            old_folder = os.path.join(root, 'attachments')
            new_folder = os.path.join(root, 'assets')
            # 如果目标文件夹已存在则删除
            if os.path.exists(new_folder):
                shutil.rmtree(new_folder)
            os.rename(old_folder, new_folder)

    # 第三步：更新图片引用路径 attachments/ -> assets/
    for root, dirs, files in os.walk('new'):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 替换 ![](attachments/xxx) 为 ![](assets/xxx)
                new_content = re.sub(
                    r'!\[\]\(attachments/([^\)]+)\)',
                    r'![](assets/\1)',
                    content
                )
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == '__main__':
    process_md_files()
    print("处理完成！")