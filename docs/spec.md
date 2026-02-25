# Server.sh 任务管理脚本规格

## Why
需要开发一个功能完整的服务器任务管理脚本，用于在Linux/Unix系统中后台启动、停止、重启服务进程，并提供日志管理和状态查看功能。

## What Changes
- 创建 `server.sh` 主脚本，实现服务管理功能
- 创建 `test_server.py` Python测试程序作为示例可执行文件
- 创建 `README.md` 使用说明文档

## Impact
- 新增文件：`server.sh`, `test_server.py`, `README.md`
- 依赖目录：`./logs/` 用于存储日志文件

## ADDED Requirements

### Requirement: server.sh 脚本功能

#### Scenario: start - 启动服务
- **WHEN** 用户执行 `./server.sh start`
- **THEN** 
  - 检查PID文件是否存在，若存在且进程运行中则报错退出
  - 清空对应月份的日志文件
  - 在后台启动服务（调用用户定义的 start_func 函数）
  - 生成 `./server.pid` 文件写入当前进程PID
  - 输出启动成功信息

#### Scenario: stop - 优雅停止服务
- **WHEN** 用户执行 `./server.sh stop`
- **THEN**
  - 读取 `./server.pid` 获取进程ID
  - 向进程发送 SIGTERM 信号（优雅关闭）
  - 等待进程退出后删除PID文件
  - 输出停止成功信息

#### Scenario: shutdown - 强制停止服务
- **WHEN** 用户执行 `./server.sh shutdown`
- **THEN**
  - 读取 `./server.pid` 获取进程ID
  - 向进程发送 SIGKILL 信号（强制杀死）
  - 立即删除PID文件
  - 输出强制停止成功信息

#### Scenario: status - 查看服务状态
- **WHEN** 用户执行 `./server.sh status`
- **THEN**
  - 检查 `./server.pid` 文件是否存在
  - 若存在，检查对应进程是否运行
  - 显示服务状态（运行中/已停止）及PID信息

#### Scenario: log - 查看日志
- **WHEN** 用户执行 `./server.sh log [-n N] [-f]`
- **THEN**
  - 显示当前月份的日志文件内容
  - `-n N`: 显示最后N行
  - `-f`: 实时跟踪日志（tail -f 行为）

#### Scenario: restart - 重启服务
- **WHEN** 用户执行 `./server.sh restart`
- **THEN**
  - 依次执行 stop 和 start 操作

#### Scenario: clean - 清除日志
- **WHEN** 用户执行 `./server.sh clean`
- **THEN**
  - 删除 `./logs/` 目录下所有日志文件
  - 输出清理成功信息

### Requirement: 日志文件命名规则
- 日志文件格式：`./logs/server_YYYYMM.log`（如 `server_202602.log`）
- 每次启动时自动清空当月日志文件

### Requirement: PID文件管理
- PID文件路径：`./server.pid`
- 使用原子操作写入PID，避免冲突
- 服务停止后自动删除PID文件

### Requirement: 用户自定义启动函数
- 用户需在调用 server.sh 前定义 `start_func` 函数
- server.sh 的 start 命令会自动调用该函数

### Requirement: test_server.py 测试程序
- 可接收命令行参数
- 输出测试日志到标准输出
- 无限循环运行（模拟长期服务）
- 响应 SIGTERM/SIGKILL 信号优雅退出

## MODIFIED Requirements
无

## REMOVED Requirements
无
