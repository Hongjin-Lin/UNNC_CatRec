import json
import os
import requests
from urllib.parse import urljoin

"""
This script ONLY downloads cat media files based on an existing cats.json.

Data pipeline:
1) Run sync_cats_json.py to export latest records from NocoDB into ../cats.json.
2) Run this script (profile_script.py) to download photos into ../campus_cats_library.
3) Run build_profile.py to rebuild backend/data/cats.db with metadata from cats.json.
"""

# --- 配置区 ---
JSON_FILE = '../cats.json'        # 你刚才保存的文件名
BASE_URL = "http://tnr.0xnohes-l.cn:8900/"  # 基础域名
SAVE_DIR = '../campus_cats_library'  # 图片保存的根目录

# 创建根目录
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def download_cats_data():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 如果 JSON 是从 NocoDB records 抓取的，通常列表在 data['list'] 或直接是列表
    cat_list = data if isinstance(data, list) else data.get('list', [])

    print(f"开始处理，共发现 {len(cat_list)} 只猫咪...")

    for cat in cat_list:
        name = cat.get('Name', '未知猫咪').replace('/', '_') # 避免名字里有斜杠导致路径错误
        photos = cat.get('Photos', [])
        
        if not photos:
            continue

        # 为每只猫创建独立文件夹
        cat_folder = os.path.join(SAVE_DIR, name)
        if not os.path.exists(cat_folder):
            os.makedirs(cat_folder)

        print(f"正在下载 【{name}】 的照片 ({len(photos)}张)...")

        for i, photo in enumerate(photos):
            # 优先使用 path 拼接绝对地址，如果 path 报错可以尝试用 signedPath
            img_relative_path = photo.get('path')
            img_url = urljoin(BASE_URL, img_relative_path)
            
            # 构造本地保存文件名
            ext = photo.get('mimetype', 'image/jpeg').split('/')[-1]
            file_name = f"{name}_{i+1}.{ext}"
            file_path = os.path.join(cat_folder, file_name)

            # 如果文件已存在则跳过
            if os.path.exists(file_path):
                continue

            try:
                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f_img:
                        f_img.write(response.content)
                else:
                    print(f"  [失败] 无法下载: {img_url} (状态码: {response.status_code})")
            except Exception as e:
                print(f"  [错误] 下载图片时出错: {e}")

    print("\n✅ 所有照片下载完成！请查看 campus_cats_library 文件夹。")

if __name__ == "__main__":
    download_cats_data()