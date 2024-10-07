import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import todo_manager as tm
import file_utils as fu

# GUI 초기화
root = tk.Tk()
root.title('Todo List')
root.geometry('800x700')  # 세로 크기를 늘림

# 폰트 설정
FONT_LARGE = ('Helvetica', 14)

# 열 및 행 구성 설정
for i in range(3):
    root.columnconfigure(i, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(5, weight=1)  # 노트 텍스트 박스 추가를 위해 행 구성 추가

def update_todo_list():
    todo_listbox.delete(0, tk.END)
    today_listbox.delete(0, tk.END)
    completed_listbox.delete(0, tk.END)
    for idx, todo in enumerate(tm.todos):
        todo_listbox.insert(tk.END, f"{idx + 1}. {todo}")
    for idx, todo in enumerate(tm.today_todos):
        today_listbox.insert(tk.END, f"{idx + 1}. {todo}")
    for idx, todo in enumerate(tm.completed_todos):
        completed_listbox.insert(tk.END, f"{idx + 1}. {todo}")

def add_todo(event=None):
    todo = todo_entry.get()
    tm.add_todo(todo)
    todo_entry.delete(0, tk.END)
    update_todo_list()

def add_to_today():
    selected_todos = todo_listbox.curselection()
    tm.add_to_today(selected_todos)
    update_todo_list()

def check_todo():
    selected_todos = today_listbox.curselection()
    tm.check_todo_from_today(selected_todos)
    update_todo_list()

def uncheck_todo():
    selected_todos = completed_listbox.curselection()
    tm.uncheck_todo(selected_todos)
    update_todo_list()

def delete_todo(event=None):
    selected_todos = todo_listbox.curselection()
    selected_today_todos = today_listbox.curselection()
    selected_completed_todos = completed_listbox.curselection()
    
    tm.delete_todo_from_todos(selected_todos)
    tm.delete_todo_from_today(selected_today_todos)
    tm.delete_todo_completed(selected_completed_todos)
    update_todo_list()

def on_todo_double_click(event):
    add_to_today()

def on_today_double_click(event):
    check_todo()

def on_completed_double_click(event):
    uncheck_todo()

def on_todo_enter(event):
    add_to_today()

def on_today_enter(event):
    check_todo()

def on_completed_enter(event):
    uncheck_todo()

todo_entry = ttk.Entry(root, width=40)
todo_entry.grid(row=0, column=0, columnspan=3, pady=10, padx=5, sticky="ew")
todo_entry.bind("<Return>", add_todo)

add_button = ttk.Button(root, text='Add Todo', command=add_todo, width=15)
add_button.grid(row=1, column=1, pady=5, padx=5)

todo_label = ttk.Label(root, text="해야 할 일")
todo_label.grid(row=2, column=0, pady=5)

today_label = ttk.Label(root, text="오늘 할 일")
today_label.grid(row=2, column=1, pady=5)

completed_label = ttk.Label(root, text="완료된 일")
completed_label.grid(row=2, column=2, pady=5)

todo_listbox = tk.Listbox(root, width=30, height=20, selectmode=tk.EXTENDED, font=FONT_LARGE)
todo_listbox.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
todo_listbox.bind("<Double-1>", on_todo_double_click)
todo_listbox.bind("<Return>", on_todo_enter)
todo_listbox.bind("<Delete>", delete_todo)

today_listbox = tk.Listbox(root, width=30, height=20, selectmode=tk.EXTENDED, font=FONT_LARGE)
today_listbox.grid(row=3, column=1, padx=5, pady=10, sticky="nsew")
today_listbox.bind("<Double-1>", on_today_double_click)
today_listbox.bind("<Return>", on_today_enter)
today_listbox.bind("<Delete>", delete_todo)

completed_listbox = tk.Listbox(root, width=30, height=20, selectmode=tk.EXTENDED, font=FONT_LARGE)
completed_listbox.grid(row=3, column=2, padx=5, pady=10, sticky="nsew")
completed_listbox.bind("<Double-1>", on_completed_double_click)
completed_listbox.bind("<Return>", on_completed_enter)
completed_listbox.bind("<Delete>", delete_todo)

button_frame = ttk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky="ew")
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)

add_to_today_button = ttk.Button(button_frame, text='Add to Today', command=add_to_today)
add_to_today_button.grid(row=0, column=0, padx=5)

check_button = ttk.Button(button_frame, text='Check Todo', command=check_todo)
check_button.grid(row=0, column=1, padx=5)

delete_button = ttk.Button(button_frame, text='Delete Todo', command=delete_todo)
delete_button.grid(row=0, column=2, padx=5)

note_pane = ttk.PanedWindow(root, orient=tk.VERTICAL)
note_pane.grid(row=5, column=0, columnspan=3, pady=5, sticky="nsew")

note_label = ttk.Label(note_pane, text="메모")
note_pane.add(note_label)

note_textbox = tk.Text(note_pane, height=10, font=FONT_LARGE)
note_pane.add(note_textbox)

# 노트 내용을 로드
note_content = fu.load_note()
note_textbox.insert(tk.END, note_content)

tm.todos, tm.today_todos, tm.completed_todos = fu.load_todos()
fu.reset_daily_todos(tm.today_todos, tm.completed_todos)
update_todo_list()

def on_closing():
    fu.save_todos(tm.todos, tm.today_todos, tm.completed_todos)
    fu.save_note(note_textbox.get("1.0", tk.END))  # 노트 내용 저장
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
