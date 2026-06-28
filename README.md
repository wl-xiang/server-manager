# Server Manager

后台服务管理脚本，支持以守护进程方式启动任意命令，并提供停止、强制停止、状态查询、日志查看、日志滚动与清理等功能。脚本同时兼容 `sh` 与 `bash` 解释器，进程可在 SSH 终端断开后继续常驻运行。

## 项目概况

- **核心功能**：通过 `nohup` + `setsid` 将任意启动命令脱离终端会话后台运行，使用 PID 文件进行进程追踪与生命周期管理。
- **进程保活**：启动后服务进入独立会话并忽略 `SIGHUP`，SSH 断连不会导致进程退出。
- **日志管理**：每次启动自动滚动日志，按配置保留若干份历史备份。
- **配置隔离**：通过 `.env` 文件管理环境变量配置，代码与配置分离。
- **统一输出**：所有控制台输出均为英文，避免终端编码乱码。

## 目录结构

```
.
├── server          # 服务管理脚本（主入口）
├── test_server.py  # 用于测试的示例服务
├── .env.example    # 环境变量配置模板
├── .gitignore
└── README.md
```

## 快速开始

### 1. 准备配置

复制配置模板并填写启动命令：

```bash
cp .env.example .env
# 编辑 .env，填写 START_COMMAND 等
```

### 2. 启动服务

```bash
./server start
```

启动后服务将在后台运行，PID 记录于 `server.pid`，日志写入 `logs/server.log`。

### 3. 常用命令

```bash
# 启动服务（带前后钩子命令）
./server start \
  --command "python3 test_server.py" \
  --before "echo 'Starting server...'" \
  --after "echo 'Server started'"

# 查看状态
./server status

# 查看日志
./server logs              # 查看全部日志
./server logs -n 50        # 查看最后 50 行
./server logs -f           # 实时跟踪日志

# 停止服务
./server stop              # 优雅停止 (SIGTERM)
./server shutdown          # 强制停止 (SIGKILL)

# 重启服务
./server restart

# 清理日志
./server clean
```

## 命令说明

| 命令 | 说明 |
|------|------|
| `start` | 后台启动服务，进程脱离终端会话常驻运行 |
| `stop` | 优雅停止服务 (SIGTERM)，默认等待最多 30 秒 |
| `shutdown` | 强制停止服务 (SIGKILL) |
| `status` | 查看服务运行状态 |
| `logs` | 查看日志，支持 `-n NUM` 指定行数与 `-f` 实时跟踪 |
| `restart` | 重启服务（未运行时直接启动） |
| `clean` | 清理全部日志文件（服务运行时禁止清理） |

### start 选项

| 选项 | 说明 |
|------|------|
| `-c, --command CMD` | 设置启动命令 |
| `-b, --before CMD` | 启动前执行的命令 |
| `-a, --after CMD` | 启动后执行的命令 |

## 环境变量配置

所有可配置参数均通过 `.env` 文件暴露，模板见 `.env.example`。

| 变量 | 是否必填 | 默认值 | 说明 |
|------|----------|--------|------|
| `START_COMMAND` | 必填 | - | 启动命令 |
| `BEFORE_COMMAND` | 可选 | 空 | 启动前执行的命令 |
| `AFTER_COMMAND` | 可选 | 空 | 启动后执行的命令 |
| `LOG_DIR` | 可选 | `logs` | 日志目录，相对路径基于脚本目录 |
| `LOG_FILE_NAME` | 可选 | `server.log` | 日志文件名 |
| `LOG_MAX_BACKUPS` | 可选 | `2` | 日志备份保留份数 |

### 配置规则

- **必填参数**：在 `.env` 中留空，需通过环境变量或命令行参数提供。
- **可选参数**：模板中已写入默认值，日志配置类参数均已配置默认值。
- **优先级**：环境变量（`.env` 或 shell 中导出）设置且非空时，优先级高于命令行参数。
- **值处理**：`.env` 中的值按字面量读取，不进行 shell 变量展开；含空格的值可直接书写或用引号包裹（`KEY=a b c` 与 `KEY="a b c"` 等效）。以 `#` 开头的行视为注释。如需变量展开，请在 shell 中 `export` 后启动。

### 配置示例

```bash
# .env
START_COMMAND=python3 test_server.py
BEFORE_COMMAND=echo "Preparing environment..."
AFTER_COMMAND=
LOG_DIR=logs
LOG_FILE_NAME=server.log
LOG_MAX_BACKUPS=5
```

也可以不使用 `.env`，直接在命令行或通过环境变量启动：

```bash
# 命令行参数
./server start --command "python3 test_server.py"

# 环境变量
export START_COMMAND="python3 test_server.py"
./server start
```

## 日志管理

日志文件位置：`logs/server.log`（可通过 `LOG_DIR` / `LOG_FILE_NAME` 修改）。

### 日志滚动

每次启动服务时自动滚动：

- `server.log` — 当前日志
- `server.log.bak.1` — 最近一次备份
- `server.log.bak.2` — 第二次备份
- ...

默认保留 2 份备份，可通过 `LOG_MAX_BACKUPS` 修改。

### 清理日志

```bash
./server clean   # 清理所有日志文件
```

> **注意**：服务运行时无法清理日志，需先停止服务。

## 进程保活说明

`start` 命令通过以下机制保证服务在 SSH 断连后继续运行：

1. `setsid` 创建新的会话，脱离终端控制。
2. `nohup` 忽略 `SIGHUP` 信号（`setsid` 不可用时自动回退至 `nohup`）。
3. 标准输入重定向至 `/dev/null`，标准输出与错误输出重定向至日志文件。

因此执行 `server start` 后即可安全关闭终端，服务会持续在后台运行。

## 兼容性说明

- 脚本以 `#!/bin/sh` 启动，仅使用 POSIX 兼容语法，可同时在 `sh` 与 `bash` 下运行。
- 不依赖 `[[ ]]`、`BASH_SOURCE`、`echo -e`、`disown` 等 bash 专属语法。
