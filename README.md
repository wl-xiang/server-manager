# Server Manager

后台服务管理脚本，支持启动、停止、查看日志、日志滚动等功能。

## 使用方式

### 1. 启动命令

#### 方式一：命令行参数
```bash
./server start --command "python3 your_server.py"
```

#### 方式二：环境变量
```bash
export START_COMMAND="python3 your_server.py"
./server start
```

### 2. 完整示例

```bash
# 启动服务（带前后钩子命令）
./server start \
  --command "python3 server.py" \
  --before "echo 'Starting server...'" \
  --after "echo 'Server started'"

# 查看状态
./server status

# 查看日志
./server logs              # 查看全部日志
./server logs -n 50       # 查看最后50行
./server logs -f          # 实时跟踪日志

# 停止服务
./server stop            # 优雅停止 (SIGTERM)
./server shutdown        # 强制停止 (SIGKILL)

# 重启
./server restart

# 清理日志
./server clean
```

## 命令行选项

| 选项 | 说明 |
|------|------|
| `-c, --command CMD` | 设置启动命令 |
| `-b, --before CMD` | 启动前执行的命令 |
| `-a, --after CMD` | 启动后执行的命令 |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `START_COMMAND` | 启动命令 | - |
| `BEFORE_COMMAND` | 启动前命令 | - |
| `AFTER_COMMAND` | 启动后命令 | - |
| `LOG_MAX_BACKUPS` | 日志备份份数 | 2 |

**优先级**：环境变量 > 命令行参数

## 日志管理

日志文件位置：`logs/server.log`

### 日志滚动

每次启动服务时自动滚动：
- `server.log` - 当前日志
- `server.log.bak.1` - 最近一次备份
- `server.log.bak.2` - 第二次备份
- ...

默认保留2份备份，可通过 `LOG_MAX_BACKUPS` 环境变量修改：

```bash
export LOG_MAX_BACKUPS=5
./server start --command "python3 server.py"
```

### 清理日志

```bash
./server clean   # 清理所有日志文件
```

**注意**：服务运行时无法清理日志，需先停止服务。
