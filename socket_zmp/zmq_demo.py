import zmq
import time
import threading

# ZMQ 通信示例

# 服务端函数
def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    
    print("服务器已启动，等待客户端连接...")
    
    try:
        while True:
            # 等待客户端请求
            message = socket.recv_string()
            print(f"收到请求: {message}")
            
            # 处理请求（这里简单地等待1秒模拟处理过程）
            time.sleep(1)
            
            # 发送回复
            socket.send_string(f"服务器回复: {message}")
    except KeyboardInterrupt:
        print("服务器关闭")
    finally:
        socket.close()
        context.term()

# 客户端函数
def client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    
    print("客户端已启动，开始发送请求...")
    
    try:
        for i in range(1):
            message = f"请求 #{i}"
            print(f"发送: {message}")
            
            # 发送请求
            socket.send_string(message)
            
            # 等待回复
            response = socket.recv_string()
            print(f"收到回复: {response}")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("客户端关闭")
    finally:
        socket.close()
        context.term()

# 主函数
def main():
    # 创建服务器线程
    server_thread = threading.Thread(target=server)
    server_thread.daemon = True
    server_thread.start()
    
    # 给服务器一点时间启动
    time.sleep(1)
    
    # 运行客户端
    client()

if __name__ == "__main__":
    main()
