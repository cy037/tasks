def add_task(tasks, title):
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1
    else:
        new_id = 1

    task = {
        "id": new_id,
        "title": title,
        "done": False
    }

    tasks.append(task)
    return task


# 4. 查看任务
def list_tasks(tasks):
    if not tasks:
        print("当前没有任务")
        return

    print("\n===== 任务列表 =====")

    for task in tasks:
        if task["done"]:
            status = "已完成"
        else:
            status = "未完成"

        print(f'ID: {task["id"]} | '
              f'任务: {task["title"]} | '
              f'状态: {status}')

    print("====================")


# 5. 完成任务
def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                return "already_done"

            task["done"] = True
            return "success"

    return "not_found"


# 6. 删除任务
def delete_task(tasks, task_id):


    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True

    return False

def edit_task(tasks, task_id, new_title):
    
    for task in tasks:
        
        if task["id"] == task_id:
            
            task["title"] = new_title                                       
            return True
    
    return False