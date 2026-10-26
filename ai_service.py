
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:1.5b"


def extract_task_from_ai(user_input):
    """使用 Ollama 提取任务标题、开始时间和结束时间。"""

    prompt = f"""
你是一个任务信息提取助手。
请从用户输入中提取任务标题、开始时间和结束时间。

规则：
1. title：只保留任务本身，不包含时间信息。
2. start_time：开始时间，统一使用 24 小时制 HH:MM 格式。
3. end_time：结束时间，统一使用 24 小时制 HH:MM 格式。
4. 用户没有提供开始或结束时间时，对应字段返回空字符串。
5. 不要猜测用户没有提供的时间。
6. 忽略日期信息，例如“明天”“后天”，因为当前版本不保存日期。
7. 只返回 JSON，不要输出解释。

示例：
输入：明天上午九点学习 FastAPI
输出：{{"title":"学习 FastAPI","start_time":"09:00","end_time":""}}

输入：下午两点到四点学习 Python
输出：{{"title":"学习 Python","start_time":"14:00","end_time":"16:00"}}

输入：整理项目代码
输出：{{"title":"整理项目代码","start_time":"","end_time":""}}

用户输入：{user_input}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "start_time": {"type": "string"},
                "end_time": {"type": "string"}
            },
            "required": ["title", "start_time", "end_time"]
        },
        "think": False,
        "options": {"temperature": 0}
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        ai_text = response.json().get("response", "")
        print("AI 原始返回内容：", repr(ai_text))

        task_info = json.loads(ai_text)

        title = task_info.get("title", "").strip()
        start_time = task_info.get("start_time", "").strip()
        end_time = task_info.get("end_time", "").strip()

        if not title:
            return {
                "title": "",
                "start_time": "",
                "end_time": ""
            }

        return {
            "title": title,
            "start_time": start_time,
            "end_time": end_time
        }

    except (requests.RequestException, json.JSONDecodeError, ValueError) as exc:
        print(f"AI 服务调用或解析失败：{exc}")
        return None
