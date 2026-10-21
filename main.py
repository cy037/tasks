from storage import load_tasks, save_tasks
from tasks_ser import add_task, list_tasks, complete_task, delete_task


def main():
    tasks = load_tasks()

    # 如果任务文件损坏，停止运行，避免意外覆盖原文件
    if tasks is None:
        print("程序已停止，请修复任务文件后再运行。")
        return

    while True:
        print("欢迎使用任务管理器！")
        print("\n===== 任务管理器 =====")
        print("1. 查看任务")
        print("2. 添加任务")
        print("3. 完成任务")
        print("4. 删除任务")
        print("0. 退出程序")

        choice = input("请输入选项：").strip()

        # 查看任务
        if choice == "1":
            list_tasks(tasks)

        # 添加任务
        elif choice == "2":
            title = input("请输入任务名称：").strip()

            if not title:
                print("任务名称不能为空")
                continue

            task = add_task(tasks, title)
            save_tasks(tasks)

            print(f'添加成功，任务 ID 为 {task["id"]}')

        # 完成任务
        elif choice == "3":
            try:
                task_id = int(input("请输入要完成的任务 ID："))
            except ValueError:
                print("ID 必须是整数")
                continue

            result = complete_task(tasks, task_id)

            if result == "success":
                save_tasks(tasks)
                print("任务已完成")
            elif result == "already_done":
                print("这个任务已经完成了")
            else:
                print("未找到该任务")

        # 删除任务
        elif choice == "4":
            try:
                task_id = int(input("请输入要删除的任务 ID："))
            except ValueError:
                print("ID 必须是整数")
                continue

            result = delete_task(tasks, task_id)

            if result:
                save_tasks(tasks)
                print("任务删除成功")
            else:
                print("未找到该任务")

        # 退出程序
        elif choice == "0":
            print("程序已退出")
            break

        else:
            print("无效选项，请重新输入")


if __name__ == "__main__":
    main()