# Pixel Chat Backend

一个基于Python FastAPI的实时聊天后台系统，支持WebSocket实时通信。

## 功能特性

- 🚀 实时聊天：基于WebSocket的实时消息传递
- 👥 用户管理：创建和管理用户
- 🏠 聊天室：支持多个聊天室
- 💬 消息历史：保存和获取聊天记录
- 🌐 跨域支持：支持前端跨域访问
- 📱 响应式前端：简洁美观的聊天界面

## 技术栈

- **后端框架**: FastAPI
- **WebSocket**: 实时通信
- **数据存储**: 内存存储（可扩展为数据库）
- **前端**: HTML + CSS + JavaScript

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务器

```bash
python main.py
```

或者使用uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问应用

打开浏览器访问：http://localhost:8000

## API接口

### 用户管理

- `POST /users` - 创建新用户
- `GET /users` - 获取所有用户列表

### 聊天室管理

- `GET /rooms` - 获取所有聊天室
- `GET /rooms/{room_id}` - 获取特定聊天室信息
- `POST /rooms` - 创建新聊天室
- `GET /rooms/{room_id}/messages` - 获取聊天室消息历史

### WebSocket

- `WS /ws/{user_id}` - WebSocket连接端点

## 前端使用

1. 在登录页面输入用户名
2. 点击"进入聊天"按钮
3. 开始实时聊天

## 消息格式

### 发送消息格式

```json
{
    "type": "chat",
    "room_id": "room_id",
    "content": "消息内容"
}
```

### 接收消息格式

```json
{
    "type": "chat",
    "message": {
        "id": "message_id",
        "room_id": "room_id",
        "user_id": "user_id",
        "username": "用户名",
        "content": "消息内容",
        "timestamp": "2023-12-01T10:00:00"
    }
}
```

## 项目结构

```
backend/
├── main.py              # 主应用文件
├── requirements.txt     # 依赖文件
├── static/             # 静态文件目录
│   └── index.html      # 前端页面
└── README.md           # 项目说明
```

## 扩展功能

- 数据库集成（SQLite/PostgreSQL）
- 用户认证和授权
- 文件上传和图片分享
- 私聊功能
- 消息加密
- 在线状态显示

## 开发说明

这是一个基础版本的聊天系统，数据存储在内存中。在生产环境中，建议：

1. 使用数据库存储用户和消息数据
2. 添加用户认证和授权
3. 实现消息持久化
4. 添加错误处理和日志记录
5. 配置适当的安全措施

## 许可证

MIT License
