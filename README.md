# Web Strace

基于 Web 的 strace 实时追踪与分析工具。通过浏览器实时查看进程的系统调用，支持分类统计、耗时分析和历史回放。

## 系统要求

- Linux（需要 strace 已安装：`/usr/bin/strace`）
- Python 3.10+
- 现代浏览器（Chrome/Firefox/Edge）

## 项目结构

```
web_strace/
├── backend/          # FastAPI 后端
│   ├── main.py       # 路由与主逻辑
│   ├── runner.py     # strace 进程管理
│   ├── parser.py     # strace 输出解析
│   ├── analyzer.py   # 系统调用分类与严重度评估
│   ├── session.py    # SQLite 会话存储
│   ├── websocket.py  # WebSocket 连接管理
│   ├── models.py     # 数据模型
│   └── requirements.txt
├── frontend/         # Vue 3 前端（单文件，CDN 引入）
│   └── index.html
└── data/             # 运行时自动生成，SQLite 数据库
```

## 安装与运行

### 1. 安装依赖

```bash
cd web_strace
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. 启动服务

```bash
source .venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

注意：strace 需要 root 权限或 `CAP_SYS_PTRACE`，如果追踪的是其他用户的进程，需要用 `sudo` 启动：

```bash
sudo .venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 3. 访问前端

浏览器打开 `http://localhost:8000`

## 功能说明

### 实时追踪

1. 在输入框中输入要追踪的命令（如 `ls -la /tmp`）
2. 点击"开始追踪"，页面会实时显示系统调用事件流
3. 运行时间实时刷新
4. 支持按分类过滤（文件/I/O/网络/进程/内存/同步/信号）
5. 支持文本搜索过滤
6. 自动统计各分类调用数、占比及耗时最长的调用

### 历史记录

- 切换到"历史记录"标签查看所有执行过的追踪
- 点击历史条目可以回放对应的系统调用数据
- 如果历史会话仍在运行中，会自动重新连接 WebSocket 获取实时数据

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/start` | 创建追踪会话，body: `{"command": "..."}` |
| POST | `/api/start/{session_id}` | 启动追踪 |
| POST | `/api/stop/{session_id}` | 停止追踪 |
| GET  | `/api/sessions` | 获取所有会话列表 |
| GET  | `/api/sessions/{session_id}` | 获取单个会话信息 |
| GET  | `/api/sessions/{session_id}/events` | 获取会话事件，支持 `limit` 和 `offset` 参数 |
| WS   | `/ws/{session_id}` | WebSocket 实时推送 |

### WebSocket 消息格式

```json
// 事件批次
{"type": "batch", "data": [{...event}, ...]}

// 统计数据
{"type": "stats", "data": {"total_count": N, "category_counts": {...}, ...}}

// 状态变更
{"type": "status", "data": {"state": "running|finished|error", "message": ""}}
```

## 技术栈

- **后端**：FastAPI + WebSocket + SQLite
- **前端**：Vue 3（CDN 引入，无需构建工具）
- **通信**：WebSocket 实时推送 + REST API 历史查询
