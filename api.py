import asyncio
import threading
from flask import Flask, render_template
from flask_cors import CORS
import websockets

# 创建 Flask 应用程序
app = Flask(__name__)
CORS(app)

# 定义一个全局的客户端连接集合，用于存储所有的客户端连接
clients = set()

# 定义处理 WebSocket 连接请求的协程函数
async def handle_client(websocket, path):
    # 存储客户端的连接
    clients.add(websocket)
    print(f'新的客户端已连接：{websocket.remote_address}')
    try:
        # 循环接收客户端发送的消息
        async for message in websocket:
            # 将消息广播给所有客户端
            for client in clients:
                await client.send(f'{websocket.remote_address}发送的{message}_666啊')
            print(f'客户端 {websocket.remote_address} 发送了消息：{message}')
    finally:
        # 当客户端关闭连接时，从连接列表中删除该连接
        clients.remove(websocket)
        print(f'客户端已断开连接：{websocket.remote_address}')

# 定义启动 WebSocket 服务器的函数
def start_websocket_server():
    # 启动事件循环
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(handle_client, 'localhost', 5100)
    print('WebSocket 服务器已启动，正在监听端口 5100...')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# 在 Flask 中定义一个路由，用于返回一个简单的 HTML 页面，页面中包含 JavaScript 代码，用于连接 WebSocket 服务器并发送消息
@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    # 创建一个新线程，用于启动 WebSocket 服务器
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.start()
    # 启动 Flask 应用程序
    app.run()
