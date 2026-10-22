from fastapi import FastAPI
import tasks_ser
import storage
from pydantic import BaseModel


app = FastAPI()
class TaskCreate(BaseModel):
    title: str


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

