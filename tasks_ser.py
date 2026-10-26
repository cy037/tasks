
from database import get_connection
import requests
import json
import re


VALID_STATUSES = {"todo", "done"}


def add_task(title, start_time="", end_time="", details="", status="todo"):
    """新增任务，返回新任务的 ID。"""
    title = title.strip()

    if not title:
        raise ValueError("任务标题不能为空")

    if status not in VALID_STATUSES:
        raise ValueError("任务状态只能是 todo 或 done")

    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO tasks
                (title, start_time, end_time, details, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, start_time, end_time, details, status)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def list_tasks():
    """查询所有任务，按 ID 从新到旧排列。"""
    conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_task(task_id):
    """根据 ID 查询单个任务，不存在时返回 None。"""
    conn = get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return dict(row) if row else None
    finally:
        conn.close()


def complete_task(task_id):
    """将任务标记为已完成。"""
    conn = get_connection()

    try:
        cursor = conn.execute(
            "UPDATE tasks SET status = 'done' WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_task(task_id):
    """删除任务，返回是否成功找到并删除记录。"""
    conn = get_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_task(task_id, new_title, new_status="todo"):
    """修改任务标题和状态。"""
    new_title = new_title.strip()

    if not new_title:
        raise ValueError("任务标题不能为空")

    if new_status not in VALID_STATUSES:
        raise ValueError("任务状态只能是 todo 或 done")

    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE tasks
            SET title = ?, status = ?
            WHERE id = ?
            """,
            (new_title, new_status, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def extract_task_from_ai(user_input):
    # 升级版 Prompt：要求 AI 提取所有字段，并严格输出 JSON
    prompt = f"""
    你是一个严格的任务提取程序。请从用户的输入中提取任务信息，并严格输出 JSON 格式。
    你需要提取以下字段：
    - title: 任务核心标题 (必填)
    - start_time: 开始时间 (如果没有提，填空字符串 "")
    - end_time: 结束时间 (如果没有提，填空字符串 "")
    - details: 任务细节 (如果没有提，填空字符串 "")
    
    注意：绝对不能输出任何思考过程，不要解释，只输出 JSON。
    格式示例：{{"title": "写周报", "start_time": "明天下午3点", "end_time": "", "details": "总结项目进度"}}

    用户输入：{user_input}
    输出："""

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:1.5b", 
        "prompt": prompt,
        "stream": False
    }

    try:
        # 保留上次修复的强制直连代码，防代理拦截
        response = requests.post(url, json=payload, timeout=120, proxies={"http": None, "https": None})
        result_text = response.json().get("response", "")
        
        # 打印出来看看 AI 到底回了啥（调试用）
        print("\n🤖 AI 的原始回复是：", result_text, "\n")

        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data  # 注意：这里返回的是整个字典 data，不再是 data.get("title")
        return None      # 如果连大括号都没匹配到，返回 None
    except Exception as e:
        print(f"AI 解析出错: {e}")
        return None