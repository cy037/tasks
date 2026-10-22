import tasks_ser

# 测试添加任务
def test_add_task():
    tasks = []
    # 假设你的 add_task 函数不需要返回，我们通过检查列表来判断
    tasks_ser.add_task(tasks, "学习 pytest")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "学习 pytest"
    assert tasks[0]["done"] == False

# 测试修改任务（正常情况）
def test_edit_task_success():
    tasks = [{"id": 1, "title": "旧标题", "done": False}]
    result = tasks_ser.edit_task(tasks, 1, "新标题")
    assert result == True
    assert tasks[0]["title"] == "新标题"

# 测试修改任务（失败情况：ID不存在）
def test_edit_task_not_found():
    tasks = [{"id": 1, "title": "旧标题", "done": False}]
    result = tasks_ser.edit_task(tasks, 99, "新标题")
    assert result == False  # 必须返回 False
    assert tasks[0]["title"] == "旧标题" # 原有数据不能被破坏