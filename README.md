# Server 管理脚本使用说明

本脚本用于管理后台服务进程，支持启动、停止、重启、日志查看等功能。

## 快速开始

### 1. 复制模板文件

```bash
cp server.template server
chmod +x server
```

### 2. 实现 start_func 函数

在 `server` 中找到 `start_func()` 函数，按需修改启动命令：

```bash
start_func() {
    # 在这里启动你的服务进程
    # 示例：启动 Python 程序
    python3 /path/to/your/server.py >> "${LOG_FILE}" 2>&1

    # 示例：启动 Node.js 服务
    # node /path/to/your/server.js >> "${LOG_FILE}" 2>&1

    # 示例：启动 Java 程序
    # java -jar /path/to/your/app.jar >> "${LOG_FILE}" 2>&1
}
```

**注意**：
- `${LOG_FILE}` 是自动生成的日志文件路径，格式为 `./logs/server_YYYYMM.log`
- 确保你的服务程序会持续运行（不要自动退出）
- 建议处理 SIGTERM 信号以支持优雅停止

## 命令说明

| 命令 | 说明 |
|------|------|
| `./server start` | 后台启动服务 |
| `./server stop` | 优雅停止服务（SIGTERM） |
| `./server shutdown` | 强制停止服务（SIGKILL） |
| `./server status` | 查看服务运行状态 |
| `./server restart` | 重启服务 |
| `./server log` | 查看日志 |
| `./server clean` | 清除所有日志文件 |

### start - 启动服务

```bash
./server start
```

- 检查服务是否已运行
- 清空当月日志文件
- 在后台启动服务
- 生成 `server.pid` 文件记录进程ID

### stop - 优雅停止

```bash
./server stop
```

- 向服务进程发送 SIGTERM 信号
- 等待服务正常退出（最多30秒）
- 删除 PID 文件

### shutdown - 强制停止

```bash
./server shutdown
```

- 向服务进程发送 SIGKILL 信号
- 立即杀死进程（不等待）
- 删除 PID 文件

**注意**：强制停止可能导致数据丢失，建议优先使用 `stop`

### status - 查看状态

```bash
./server status
```

输出示例：
- 运行中：`Server is running (PID: 12345)`
- 已停止：`Server is stopped`

### restart - 重启服务

```bash
./server restart
```

依次执行 `stop` 和 `start`，服务会使用新的进程ID运行。

### log - 查看日志

```bash
# 查看全部日志
./server log

# 查看最后 N 行
./server log -n 100

# 实时跟踪日志（类似 tail -f）
./server log -f

# 实时跟踪最后 N 行
./server log -n 50 -f
```

日志文件自动命名为 `logs/server_YYYYMM.log`，按年月轮转。

### clean - 清除日志

```bash
./server clean
```

- 删除 `logs/` 目录下所有 `server_*.log` 日志文件
- 服务运行时无法执行（会报错）

## 文件结构

```
.
├── server.template    # 模板文件
├── server       # 你的服务脚本（复制后）
├── server.pid        # PID 文件（运行时生成）
├── logs/             # 日志目录
│   └── server_YYYYMM.log
└── test_server.py    # 测试用程序
```

## 信号处理建议

为了让你的服务支持优雅停止，建议在代码中处理 SIGTERM 信号：

**Python 示例**：
```python
import signal
import sys

running = True

def signal_handler(signum, frame):
    global running
    print("Received SIGTERM, shutting down...")
    running = False

signal.signal(signal.SIGTERM, signal_handler)

while running:
    # 你的业务逻辑
    pass
```

**Node.js 示例**：
```javascript
process.on('SIGTERM', () => {
    console.log('Received SIGTERM, shutting down...');
    process.exit(0);
});
```

## 常见问题

**Q: 启动时报错 "Error: Server is already running"**
A: 服务已在运行，先执行 `./server stop` 停止后再启动。

**Q: 停止服务失败**
A: 服务可能无法响应 SIGTERM，可以尝试 `./server shutdown` 强制停止。

**Q: 日志文件在哪**
A: 日志文件在 `logs/server_YYYYMM.log`，其中 YYYYMM 是当前年月。
