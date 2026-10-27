
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import ai_service
import tasks_ser
from database import init_db


app = FastAPI(
    title="任务管理器 API",
    version="2.1.0"
)


@app.on_event("startup")
def startup():
    """应用启动时初始化数据库。"""
    init_db()


class AIPrompt(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    start_time: str = ""
    end_time: str = ""
    details: str = ""
    status: Literal["todo", "done"] = "todo"


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: Literal["todo", "done"] = "todo"


def handle_service_error(exc):
    """记录内部异常，并返回通用服务器错误。"""
    print(f"任务服务发生异常：{exc}")
    raise HTTPException(
        status_code=500,
        detail="服务器内部错误，请稍后重试"
    ) from exc


@app.get("/tasks")
def get_tasks():
    """获取全部任务。"""
    try:
        return tasks_ser.list_tasks()
    except Exception as exc:
        handle_service_error(exc)


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """手动创建任务。"""
    try:
        task_id = tasks_ser.add_task(
            title=task.title,
            start_time=task.start_time,
            end_time=task.end_time,
            details=task.details,
            status=task.status
        )

        return {
            "message": "添加成功",
            "id": task_id
        }

    except Exception as exc:
        handle_service_error(exc)


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """获取单个任务。"""
    try:
        tasks = tasks_ser.list_tasks()

        for task in tasks:
            if task["id"] == task_id:
                return task

        raise HTTPException(
            status_code=404,
            detail="任务不存在"
        )

    except HTTPException:
        raise
    except Exception as exc:
        handle_service_error(exc)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    """修改任务标题和状态。"""
    try:
        success = tasks_ser.update_task(
            task_id=task_id,
            new_title=task.title,
            new_status=task.status
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail="任务不存在"
            )

        return {"message": "修改成功"}

    except HTTPException:
        raise
    except Exception as exc:
        handle_service_error(exc)


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    """删除任务。"""
    try:
        success = tasks_ser.delete_task(task_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="任务不存在"
            )

        return {"message": "删除成功"}

    except HTTPException:
        raise
    except Exception as exc:
        handle_service_error(exc)


@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    """将任务标记为完成。"""
    try:
        success = tasks_ser.complete_task(task_id)
        

        if not success:
            raise HTTPException(
                status_code=404,
                detail="任务不存在"
            )

        return {"message": "任务已完成"}

    except HTTPException:
        raise
    except Exception as exc:
        handle_service_error(exc)


@app.post("/tasks/ai", status_code=201)
def create_task_with_ai(request: AIPrompt):
    """通过 AI 提取标题和时间，并创建任务。"""
    try:
        task_info = ai_service.extract_task_from_ai(
            request.prompt.strip()
        )

        if task_info is None:
            raise HTTPException(
                status_code=502,
                detail="AI 服务调用失败，请检查 Ollama 是否正在运行"
            )

        title = task_info.get("title", "").strip()
        start_time = task_info.get("start_time", "").strip()
        end_time = task_info.get("end_time", "").strip()

        if not title:
            raise HTTPException(
                status_code=422,
                detail="AI 没有提取到有效任务，请换一种说法"
            )

        task_id = tasks_ser.add_task(
            title=title,
            start_time=start_time,
            end_time=end_time
        )

        return {
            "status": "success",
            "message": "AI 已成功创建任务",
            "task": {
                "id": task_id,
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "status": "todo"
            }
        }

    except HTTPException:
        raise
    except Exception as exc:
        handle_service_error(exc)
