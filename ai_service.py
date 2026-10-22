import requests
import json
import re

def extract_task_from_ai(user_input):
    # 我们要求 AI 只输出 JSON 格式，方便程序解析
    prompt = f"""
    你是一个我的任务助手。请从下面这句话中提取出要做的任务，并输出严格的 JSON 格式。
    不要输出任何解释，不要加 markdown 的代码块符号，直接输出格式如：{{"title": "提取出的任务"}}
    如果提取不到任务，输出 {{"title": ""}}
    
    用户输入：{user_input}
    """

    # 调用本地 Ollama（端口默认是 11434，模型名字根据你本地实际的来，比如 deepseek-r1:1.5b）
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-r1:1.5b", 
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        result_text = response.json().get("response", "")
        
        # DeepSeek-R1 可能会输出思考过程（如 ...），我们提取大括号里的内容
        # 使用正则提取第一个 { 到最后一个 } 之间的内容
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data.get("title", "")
        return ""
    except Exception as e:
        print(f"AI 解析出错: {e}")
        return None