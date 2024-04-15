"""
@file: tasks.py
@time: 2024/4/2 15:06
@desc: 
"""


from celery import Celery

# 配置Celery使用RabbitMQ作为消息代理
app = Celery('tasks', broker='amqp://guest:guest@localhost//', backend="redis://localhost:6379/0")

# 创建一个名为add的任务
@app.task
def add(x, y):
    return x + y
