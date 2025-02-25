import tkinter as tk
from tkinter import messagebox
import os
import json
from datetime import datetime

TODO_FILE = 'todo_list.json'

# 加载待办事项列表
def load_todo_list():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    return []

# 保存待办事项列表
def save_todo_list():
    with open(TODO_FILE, 'w') as f:
        json.dump(todo_list, f)

# 添加任务
def add_task():
    task = entry_task.get()
    if task:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        todo_list.append({'task': task, 'details': '', 'completed': False, 'timestamp': timestamp})
        save_todo_list()
        entry_task.delete(0, tk.END)
        update_task_listbox()
    else:
        messagebox.showwarning("输入错误", "任务不能为空")

# 删除任务
def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        del todo_list[task_index]
        save_todo_list()
        update_task_listbox()
        hide_details()
    else:
        messagebox.showwarning("选择错误", "请先选择一个任务")

# 标记任务为完成
def complete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        todo_list[task_index]['completed'] = True
        save_todo_list()
        update_task_listbox()
    else:
        messagebox.showwarning("选择错误", "请先选择一个任务")

# 显示任务细节
def show_details(event):
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        task_details = todo_list[task_index].get('details', '')
        text_details.delete(1.0, tk.END)
        text_details.insert(tk.END, task_details)
        text_details.pack(fill=tk.BOTH, expand=True)
        scrollbar_details.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        hide_details()

# 隐藏任务细节
def hide_details(event=None):
    text_details.pack_forget()
    scrollbar_details.pack_forget()

# 更新任务列表框
def update_task_listbox():
    listbox_tasks.delete(0, tk.END)
    for item in todo_list:
        status = "✓" if item['completed'] else "✗"
        timestamp = item['timestamp']
        listbox_tasks.insert(tk.END, f"{status} {item['task']} ({timestamp})")

# 更新任务细节
def update_task_details(event=None):
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        todo_list[task_index]['details'] = text_details.get(1.0, tk.END)
        save_todo_list()

# 创建主窗口
root = tk.Tk()
root.title("待办事项列表")

# 创建任务输入框
entry_task = tk.Entry(root, width=50)
entry_task.pack(pady=10)

# 创建任务列表框和滚动条
frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10)

scrollbar_tasks_y = tk.Scrollbar(frame_tasks)
scrollbar_tasks_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_tasks_x = tk.Scrollbar(frame_tasks, orient=tk.HORIZONTAL)
scrollbar_tasks_x.pack(side=tk.BOTTOM, fill=tk.X)

listbox_tasks = tk.Listbox(frame_tasks, width=50, height=10, yscrollcommand=scrollbar_tasks_y.set, xscrollcommand=scrollbar_tasks_x.set)
listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar_tasks_y.config(command=listbox_tasks.yview)
scrollbar_tasks_x.config(command=listbox_tasks.xview)

# 创建任务详情文本框和滚动条
frame_details = tk.Frame(root)
frame_details.pack(pady=10)

text_details = tk.Text(frame_details, width=50, height=5)
text_details.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar_details = tk.Scrollbar(frame_details, orient=tk.VERTICAL, command=text_details.yview)
scrollbar_details.pack(side=tk.RIGHT, fill=tk.Y)

text_details.config(yscrollcommand=scrollbar_details.set)

# 创建按钮框架
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# 添加任务按钮
button_add_task = tk.Button(frame_buttons, text="添加任务", command=add_task)
button_add_task.grid(row=0, column=0, padx=5)

# 删除任务按钮
button_delete_task = tk.Button(frame_buttons, text="删除任务", command=delete_task)
button_delete_task.grid(row=0, column=1, padx=5)

# 完成任务按钮
button_complete_task = tk.Button(frame_buttons, text="标记完成", command=complete_task)
button_complete_task.grid(row=0, column=2, padx=5)

# 绑定任务列表框的点击事件
listbox_tasks.bind("<<ListboxSelect>>", show_details)
text_details.bind("<Leave>", update_task_details)

# 加载初始数据并更新任务列表框
todo_list = load_todo_list()
update_task_listbox()

# 运行主循环
root.mainloop()
