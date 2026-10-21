import os
import json

#查看当前文件路径
#print("当前文件路径是:", __file__)

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "tasks.json")

def load_tasks():
    if not os.path.exists(file_path):  # 直接放 file_path 就行了
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("错误：tasks.json 文件格式损坏，请检查文件后再运行。")
        return None


# 2. 保存任务
def save_tasks(tasks):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
