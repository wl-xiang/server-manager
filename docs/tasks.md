# Tasks

## Task 1: 创建 server.sh 主脚本
- [x] 创建 server.sh 基础框架和变量定义
- [x] 实现 check_pid 函数：检查PID文件和管理进程状态
- [x] 实现 start 功能：后台启动服务并生成PID文件
- [x] 实现 stop 功能：使用SIGTERM优雅停止
- [x] 实现 shutdown 功能：使用SIGKILL强制停止
- [x] 实现 status 功能：显示服务运行状态
- [x] 实现 log 功能：支持 -n 和 -f 参数查看日志
- [x] 实现 restart 功能：依次执行stop和start
- [x] 实现 clean 功能：清除所有日志文件

## Task 2: 创建 Python 测试程序
- [x] 创建 test_server.py 可执行文件
- [x] 实现命令行参数接收
- [x] 实现日志输出功能
- [x] 实现信号处理（SIGTERM/SIGKILL）

## Task 3: 创建使用说明文档
- [x] 创建 README.md 说明文档
- [x] 包含所有功能的使用示例

## Task 4: 验证功能
- [x] 测试 start/stop 功能
- [x] 测试 status 功能
- [x] 测试 log 功能
- [x] 测试 restart 功能
- [x] 测试 clean 功能
- [x] 测试日志按月份命名

# Task Dependencies
- Task 1 完成后才开始 Task 2
- Task 1 和 Task 2 完成后开始 Task 3
- Task 1-3 完成后进行 Task 4
