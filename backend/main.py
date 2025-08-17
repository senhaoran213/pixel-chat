    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    from typing import List, Dict
    import json
    import uuid
    from datetime import datetime
    from pydantic import BaseModel
    import uvicorn
    import os

    # 数据模型
    class Message(BaseModel):
        id: str
        room_id: str
        user_id: str
        username: str
        content: str
        timestamp: datetime

    class ChatRoom(BaseModel):
        id: str
        name: str
        created_at: datetime
        messages: List[Message] = []

    class User(BaseModel):
        id: str
        username: str
        created_at: datetime

    # 全局变量
    chat_rooms: Dict[str, ChatRoom] = {}
    users: Dict[str, User] = {}
    active_connections: Dict[str, WebSocket] = {}

    app = FastAPI(title="Pixel Chat Backend", version="1.0.0")

    # CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 挂载静态文件
    if os.path.exists("static"):
        app.mount("/static", StaticFiles(directory="static"), name="static")

    # WebSocket连接管理器
    class ConnectionManager:
        def __init__(self):
            self.active_connections: Dict[str, WebSocket] = {}

        async def connect(self, websocket: WebSocket, user_id: str):
            await websocket.accept()
            self.active_connections[user_id] = websocket

        def disconnect(self, user_id: str):
            if user_id in self.active_connections:
                del self.active_connections[user_id]

        async def broadcast_to_room(self, message: str, room_id: str):
            for user_id, websocket in self.active_connections.items():
                try:
                    await websocket.send_text(message)
                except:
                    self.disconnect(user_id)

    manager = ConnectionManager()

    # 创建默认聊天室
    def create_default_room():
        room_id = str(uuid.uuid4())
        chat_rooms[room_id] = ChatRoom(
            id=room_id,
            name="公共聊天室",
            created_at=datetime.now(),
            messages=[]
        )
        return room_id

    default_room_id = create_default_room()

    @app.get("/")
    async def get():
        """返回前端页面"""
        if os.path.exists("static/index.html"):
            return FileResponse("static/index.html")
        return {"message": "Pixel Chat Backend is running!"}

    @app.get("/rooms", response_model=List[ChatRoom])
    async def get_rooms():
        """获取所有聊天室列表"""
        return list(chat_rooms.values())

    @app.get("/rooms/{room_id}", response_model=ChatRoom)
    async def get_room(room_id: str):
        """获取特定聊天室信息"""
        if room_id not in chat_rooms:
            raise HTTPException(status_code=404, detail="聊天室不存在")
        return chat_rooms[room_id]

    @app.post("/rooms")
    async def create_room(name: str):
        """创建新的聊天室"""
        room_id = str(uuid.uuid4())
        chat_rooms[room_id] = ChatRoom(
            id=room_id,
            name=name,
            created_at=datetime.now(),
            messages=[]
        )
        return {"room_id": room_id, "name": name, "message": "聊天室创建成功"}

    @app.get("/users", response_model=List[User])
    async def get_users():
        """获取所有用户列表"""
        return list(users.values())

    @app.post("/users")
    async def create_user(username: str):
        """创建新用户"""
        user_id = str(uuid.uuid4())
        users[user_id] = User(
            id=user_id,
            username=username,
            created_at=datetime.now()
        )
        return {"user_id": user_id, "username": username, "message": "用户创建成功"}

    @app.websocket("/ws/{user_id}")
    async def websocket_endpoint(websocket: WebSocket, user_id: str):
        """WebSocket连接端点"""
        await manager.connect(websocket, user_id)
        
        # 发送欢迎消息
        welcome_message = {
            "type": "system",
            "content": f"欢迎加入聊天室！",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message, default=str))
        
        try:
            while True:
                # 接收消息
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # 处理不同类型的消息
                if message_data.get("type") == "chat":
                    # 聊天消息
                    room_id = message_data.get("room_id", default_room_id)
                    content = message_data.get("content", "")
                    
                    if user_id in users:
                        username = users[user_id].username
                    else:
                        username = f"用户{user_id[:8]}"
                    
                    # 创建消息对象
                    message = Message(
                        id=str(uuid.uuid4()),
                        room_id=room_id,
                        user_id=user_id,
                        username=username,
                        content=content,
                        timestamp=datetime.now()
                    )
                    
                    # 添加到聊天室
                    if room_id in chat_rooms:
                        chat_rooms[room_id].messages.append(message)
                    
                    # 广播消息给房间内所有用户
                    broadcast_message = {
                        "type": "chat",
                        "message": {
                            "id": message.id,
                            "room_id": message.room_id,
                            "user_id": message.user_id,
                            "username": message.username,
                            "content": message.content,
                            "timestamp": message.timestamp.isoformat()
                        }
                    }
                    
                    await manager.broadcast_to_room(
                        json.dumps(broadcast_message, default=str),
                        room_id
                    )
                    
                elif message_data.get("type") == "join_room":
                    # 加入房间
                    room_id = message_data.get("room_id", default_room_id)
                    join_message = {
                        "type": "system",
                        "content": f"用户 {users.get(user_id, User(id=user_id, username=f'用户{user_id[:8]}', created_at=datetime.now())).username} 加入了聊天室",
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast_to_room(
                        json.dumps(join_message, default=str),
                        room_id
                    )
                    
        except WebSocketDisconnect:
            manager.disconnect(user_id)
            # 发送离开消息
            if user_id in users:
                leave_message = {
                    "type": "system",
                    "content": f"用户 {users[user_id].username} 离开了聊天室",
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast_to_room(
                    json.dumps(leave_message, default=str),
                    default_room_id
                )

    @app.get("/rooms/{room_id}/messages", response_model=List[Message])
    async def get_room_messages(room_id: str, limit: int = 50):
        """获取聊天室消息历史"""
        if room_id not in chat_rooms:
            raise HTTPException(status_code=404, detail="聊天室不存在")
        
        messages = chat_rooms[room_id].messages
        return messages[-limit:] if limit > 0 else messages

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
