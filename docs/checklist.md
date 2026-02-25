# Checklist

## server.sh 脚本
- [x] server.sh 文件已创建并具有可执行权限
- [x] start 功能：正确后台启动服务，生成 server.pid，清空日志文件
- [x] stop 功能：使用 SIGTERM 信号优雅停止服务
- [x] shutdown 功能：使用 SIGKILL 信号强制停止服务
- [x] status 功能：显示服务运行状态和PID信息
- [x] log 功能：支持 -n（行数）和 -f（跟踪）参数
- [x] restart 功能：依次执行 stop 和 start
- [x] clean 功能：清除所有日志文件
- [x] 日志文件按 "server_YYYYMM.log" 格式命名
- [x] PID文件管理原子性正确

## test_server.py 测试程序
- [x] test_server.py 文件已创建
- [x] 可接收命令行参数
- [x] 输出测试日志
- [x] 响应信号优雅退出
