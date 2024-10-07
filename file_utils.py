import os
import datetime

TODO_FILE = 'todo_list.txt'
NOTE_FILE = 'note.txt'

def reset_daily_todos(today_todos, completed_todos):
    if os.path.exists(TODO_FILE):
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(TODO_FILE))
        if creation_time.date() < datetime.datetime.now().date():
            today_todos.extend(completed_todos)  # 완료된 일을 다시 오늘 할 일로 이동
            completed_todos.clear()  # 완료된 일 리스트 초기화
            save_todos([], today_todos, completed_todos)  # 변경된 할 일 리스트 저장

def load_todos():
    todos = []
    today_todos = []
    completed_todos = []
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('[완료]'):
                completed_todos.append(line[4:].strip())  # [완료] 제거 후 추가
            elif line.startswith('[오늘]'):
                today_todos.append(line[4:].strip())  # [오늘] 제거 후 추가
            else:
                todos.append(line)
    return todos, today_todos, completed_todos

def save_todos(todos, today_todos, completed_todos):
    with open(TODO_FILE, 'w') as file:
        for todo in todos:
            file.write(f"{todo}\n")
        for todo in today_todos:
            file.write(f"[오늘] {todo}\n")
        for todo in completed_todos:
            file.write(f"[완료] {todo}\n")

def load_note():
    if os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, 'r') as file:
            return file.read()
    return ""

def save_note(note):
    with open(NOTE_FILE, 'w') as file:
        file.write(note)
