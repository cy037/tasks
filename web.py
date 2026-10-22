import streamlit as st
import requests

st.set_page_config(page_title="CC的任务助手", page_icon="📝", layout="centered")
st.title("CC的终端")
st.markdown("用人类的语言输入你的任务，AI 会自动帮你整理并存入系统。")

# 后端 API 的基础地址
API_BASE = "http://127.0.0.1:8000"

# --- 侧边栏：用来手动添加任务 ---
with st.sidebar:
    st.header("手动添加")
    manual_title = st.text_input("任务名称")
    if st.button("添加任务"):
        if manual_title:
            # 调用你写好的 POST /tasks 接口
            response = requests.post(f"{API_BASE}/tasks", json={"title": manual_title})
            if response.status_code == 200:
                st.success("添加成功！")
                st.rerun()  # 刷新页面以显示新数据

# --- 主界面：AI 自然语言添加 ---
st.subheader("🧠 告诉 终端 你想做什么：")
prompt = st.text_input("例如：帮我安排明天下午3点写周报", key="ai_prompt")

if st.button("🤖 让 AI 帮我添加", type="primary"):
    if prompt:
        with st.spinner("AI 正在思考中..."):
            # 调用你写好的 POST /tasks/ai 接口
            response = requests.post(f"{API_BASE}/tasks/ai", json={"prompt": prompt})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    st.success(data.get("message"))
                    st.rerun()
                else:
                    st.error(data.get("message"))
            else:
                st.error("AI 接口请求失败，请检查后端是否启动。")

st.divider()

# --- 任务列表展示 ---
st.subheader("📋 当前任务列表")

# 调用你写好的 GET /tasks 接口
try:
    response = requests.get(f"{API_BASE}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            st.info("今天没有任务，可以摸鱼了")
        else:
            for task in tasks:
                # 用 emoji 表示完成状态
                status_icon = "✅" if task["done"] else "⏳"
                st.write(f"{status_icon} **[{task['id']}]** {task['title']}")
    else:
        st.error("获取任务列表失败。")
except requests.exceptions.ConnectionError:
    st.error("无法连接到后端，请确保 FastAPI (uvicorn) 正在运行！")