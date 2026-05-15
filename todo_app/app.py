from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

FILE_NAME = 'tasks.json'

def get_moscow_time():
    # Получаем UTC время и прибавляем 3 часа
    return datetime.utcnow() + timedelta(hours=3)

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
            # Конвертируем старый формат в новый, если нужно
            converted_tasks = []
            for task in tasks:
                if isinstance(task, str):
                    # Старый формат (простая строка)
                    converted_tasks.append({
                        'text': task,
                        'date': 'Дата неизвестна'
                    })
                elif isinstance(task, dict) and 'text' in task:
                    # Новый формат
                    converted_tasks.append(task)
                else:
                    # На всякий случай
                    converted_tasks.append({
                        'text': str(task),
                        'date': 'Дата неизвестна'
                    })
            return converted_tasks
    return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear_all')
def clear_all():
    tasks.clear()
    save_tasks(tasks)
    return redirect('/')

@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form['task']
    if new_task:
        # Получаем московское время (UTC+3)
        now_msk = get_moscow_time()
        # Добавляем задачу как словарь с текстом и датой
        task_dict = {
            'text': new_task,
            'date': now_msk.strftime('%d.%m.%Y %H:%M')
        }
        tasks.append(task_dict)
        save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)