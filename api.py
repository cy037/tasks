from fastapi import FastAPI
import tasks_ser
import storage
from pydantic import BaseModel
import ai_service 


app = FastAPI()
class TaskCreate(BaseModel):
    title: str
class AIPrompt(BaseModel):
    prompt: str

@app.get("/")
async def read_root():
    return {"message": "欢迎来到cc的终端"}

@app.get("/tasks")
def get_tasks():

    tasks = storage.load_tasks()
    if tasks is None:
        tasks = []
        
    return tasks


@app.post("/tasks")
def create_task(task: TaskCreate):
    tasks = storage.load_tasks()
    if tasks is None:
        tasks = []
        
    # 调用你之前写好的函数！把客户端传来的 title 传进去
    tasks_ser.add_task(tasks, task.title)
    
    # 保存到 JSON
    storage.save_tasks(tasks)
    
    return {"message": "任务添加成功", "title": task.title}

@app.put("/tasks/{task_id}")
def edit_task(task_id:int,task:TaskCreate):
    tasks = storage.load_tasks()
    if tasks is None:
        tasks = []

    result = tasks_ser.edit_task(tasks, task_id, task.title) 
    if result:
        storage.save_tasks(tasks)
        return {"message": "任务修改成功", "task_id": task_id}
    else:
        return {"message": "未找到该任务", "task_id": task_id}   

@app.delete("/tasks/{task_id}")  # 必须是 delete
def delete_task_api(task_id: int):  # 只接收 task_id，不要 TaskCreate
    tasks = storage.load_tasks()
    if tasks is None:
        tasks = []
        
    result = tasks_ser.delete_task(tasks, task_id)
    
    if result:
        storage.save_tasks(tasks)
        return {"message": f"任务 {task_id} 删除成功"}
    else:
        return {"message": "未找到该任务"}

@app.post("/tasks/ai")
def create_task_with_ai(request: AIPrompt):  # 接收 JSON 模型
    title = ai_service.extract_task_from_ai(request.prompt) # 从模型里取 prompt
    
    if title is None:
        return {"status": "error", "message": "AI 服务连接失败，请检查 Ollama 是否启动"}
    if title == "":
        return {"status": "failed", "message": "AI 没听懂你想加什么任务"}
        
    tasks = storage.load_tasks()
    if tasks is None:
        tasks = []
        
    tasks_ser.add_task(tasks, title)
    storage.save_tasks(tasks)
    
    return {"status": "success", "message": f"AI 帮你成功添加了任务：{title}"}

