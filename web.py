import streamlit as st
import requests

st.set_page_config(page_title="CC的任务助手", page_icon="📝", layout="centered")
st.title("CC的终端")
st.markdown("用人类的语言输入你的任务，AI 会自动帮你整理并存入系统。")

API_BASE = "http://127.0.0.1:8000"

# --- 侧边栏：用来手动添加任务 ---
with st.sidebar:
    st.header("手动添加")
    manual_title = st.text_input("任务名称")
    manual_start = st.text_input("开始时间 (可选)", placeholder="例如: 14:00")
    manual_end = st.text_input("结束时间 (可选)", placeholder="例如: 16:00")
    manual_details = st.text_area("任务细节 (可选)")
    
    if st.button("添加任务"):
        if manual_title:
            payload = {
                "title": manual_title,
                "start_time": manual_start,
                "end_time": manual_end,
                "details": manual_details
            }
            response = requests.post(f"{API_BASE}/tasks", json=payload)
            # 适配后端的 201 状态码
            if response.status_code == 201:
                st.success("添加成功！")
                st.rerun()
            else:
                st.error(f"添加失败，状态码: {response.status_code}")

# --- 主界面：AI 自然语言添加 ---
st.subheader("🧠 告诉 终端 你想做什么：")
prompt = st.text_input("例如：帮我安排下午3点到5点写周报", key="ai_prompt")

if st.button("🤖 让 AI 帮我添加", type="primary"):
    if prompt:
        with st.spinner("AI 正在思考中..."):
            response = requests.post(f"{API_BASE}/tasks/ai", json={"prompt": prompt})
            
            # 适配后端的 201 状态码
            if response.status_code == 201:
                data = response.json()
                st.success(data.get("message", "AI 添加成功！"))
                st.rerun()
            else:
                st.error(f"AI 接口请求失败，状态码: {response.status_code}")

st.divider()

# --- 任务列表展示 ---
st.subheader("📋 当前任务列表")

try:
    response = requests.get(f"{API_BASE}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        if not tasks:
            st.info("今天没有任务，可以摸鱼了")
        else:
            for task in tasks:
                # 适配后端的 status 字段
                status = task.get("status", "todo")
                icon = "✅" if status == "done" else "⏳"
                
                # 折叠面板，展示新加的细节
                with st.expander(f"{icon} [{task['id']}] {task['title']}"):
                    st.write(f"**状态:** {status}")
                    st.write(f"**开始时间:** {task.get('start_time') or '未设置'}")
                    st.write(f"**结束时间:** {task.get('end_time') or '未设置'}")
                    st.write(f"**创建时间:** {task.get('created_at')}")
                    st.markdown("**细节与规划:**")
                    st.info(task.get("details") or "暂无细节")
    else:
        st.error("获取任务列表失败。")
except requests.exceptions.ConnectionError:
    st.error("无法连接到后端，请确保 FastAPI (uvicorn) 正在运行！")