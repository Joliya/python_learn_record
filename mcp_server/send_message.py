import pika

# 连接到 RabbitMQ 服务器
credentials = pika.PlainCredentials('MjpyYWJiaXRtcS1jbi0yYmw0OXcyMzEwNTpMVEFJNXRNS0xuQU5VaGlUM0Q2Qjh6amE=', 'NDNGMDFGNUI5RUIwRTNBNUY3OTJCMTA1MkFENEI5NTJDNzM1NDNDODoxNzQ3OTg1NzM0MDY2')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq-cn-2bl49w23105.cn-beijing.amqp-14.net.mq.amqp.aliyuncs.com',
        credentials=credentials,
        # 可能还需要指定虚拟主机
        # virtual_host='您的虚拟主机'
    )
)
channel = connection.channel()

# 声明队列（确保队列存在）
queue_name = 'ai_task'
channel.queue_declare(queue=queue_name)

# 发送消息
message = "Hello, RabbitMQ!"
channel.basic_publish(exchange='',
                      routing_key=queue_name,
                      body=message)

print(f" [x] Sent '{message}'")

# 关闭连接
connection.close()