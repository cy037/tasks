import tasks_ser
from database import init_db

# 每次运行测试前，确保数据库表存在
def setup_module():
    init_db()

# 测试 1：添加任务
def test_add_task():
    # 添加一条任务，拿到 ID
    task_id = tasks_ser.add_task(title="测试自动化", start_time="10:00", end_time="12:00", details="看看能不能跑通")
    assert task_id is not None
    
    # 查出来看看数据对不对
    task = tasks_ser.get_task(task_id)
    assert task["title"] == "测试自动化"
    assert task["status"] == "todo"
    
    # 清理战场（删掉刚才测试的这条）
    tasks_ser.delete_task(task_id)

# 测试 2：修改任务
def test_update_task():
    task_id = tasks_ser.add_task(title="旧名字")
    success = tasks_ser.update_task(task_id, new_title="新名字", new_status="done")
    
    assert success is True
    task = tasks_ser.get_task(task_id)
    assert task["title"] == "新名字"
    assert task["status"] == "done"
    
    tasks_ser.delete_task(task_id)

# 测试 3：传入非法数据（防御性测试）
import pytest
def test_add_empty_task():
    # 如果传空标题，必须抛出 ValueError 异常
    with pytest.raises(ValueError):
        tasks_ser.add_task(title="   ")