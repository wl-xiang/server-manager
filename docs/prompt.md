开发一个功能完整的服务器/任务管理脚本server.sh，该脚本需支持后台启动任务、进程ID管理及日志处理功能。具体实现要求如下：

1. 脚本功能规范：
   - 实现start功能：通过后台方式启动任务，生成当前目录的server.pid文件，日志输出至./logs/server_yyyymm.log（按年月自动命名）
   - 实现stop功能：优雅关闭服务（使用SIGTERM信号）
   - 实现shutdown功能：强制关闭服务（使用SIGKILL信号）
   - 实现status功能：显示服务运行状态（运行中/已停止及PID信息）
   - 实现log功能：查看最新日志文件，支持tail命令的-n（显示行数）和-f（实时跟踪）选项
   - 实现restart功能：依次执行stop和start操作
   - 实现clean功能：清除所有日志文件

2. 技术要求：
   - 启动逻辑需设计为可扩展结构，要求用户提供自定义start_func函数，供server.sh的start函数调用
   - 每次启动服务时自动truncate（清空）对应日志文件
   - 日志文件需按"server_YYYYMM.log"格式命名（如server_202311.log）
   - 确保PID文件管理的原子性，避免进程ID冲突
   - 实现完善的错误处理和用户提示

3. 测试要求：
   - 提供一个简单的Python测试程序作为可执行文件示例
   - 测试程序应能接收参数并输出测试日志
   - 验证所有脚本功能（start/stop/status等）的正确性
   - 验证日志轮转和清理功能的有效性

请完成server.sh脚本的开发，并提供配套的Python测试程序及使用说明。