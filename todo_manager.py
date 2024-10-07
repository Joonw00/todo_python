todos = []
today_todos = []
completed_todos = []

def add_todo(todo):
    if todo:
        todos.append(todo)

def add_to_today(indices):
    for index in indices:
        today_todos.append(todos[index])

def check_todo_from_today(indices):
    for index in reversed(indices):
        completed_todos.append(today_todos.pop(index))

def uncheck_todo(indices):
    for index in reversed(indices):
        today_todos.append(completed_todos.pop(index))

def delete_todo_from_todos(indices):
    for index in reversed(indices):
        todos.pop(index)

def delete_todo_from_today(indices):
    for index in reversed(indices):
        today_todos.pop(index)

def delete_todo_completed(indices):
    for index in reversed(indices):
        completed_todos.pop(index)
