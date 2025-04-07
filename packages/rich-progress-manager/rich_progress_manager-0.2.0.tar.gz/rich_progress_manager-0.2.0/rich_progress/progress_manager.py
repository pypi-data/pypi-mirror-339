# 导入系统相关模块
# 时间处理模块
import time
# 多线程支持
import threading

# 队列数据结构（用于线程间通信）
from queue import Queue
# 线程锁机制
from threading import Lock
# 类型提示支持
from typing import Optional
# Rich库控制台输出模块
from rich.console import Console
# Rich进度条相关组件
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn


class ColorLogger:
    # 定义日志级别与颜色/样式的映射关系[6](@ref)
    COLOR_MAP = {
        "INFO": ("bright_cyan", "not bold"),  # 天蓝色不加粗
        "WARNING": ("yellow", "italic"),  # 黄色斜体
        "ERROR": ("bright_red", "bold"),  # 亮红色加粗
        "SUCCESS": ("green", "bold underline"),  # 绿色加粗下划线
        "DEBUG": ("white", "dim")  # 白色暗淡
    }

    def _colorize(self, level: str, message: str) -> str:
        """格式化彩色日志消息[6](@ref)
        参数:
            level: 日志级别（INFO/ERROR等）
            message: 日志内容
        返回:
            带样式标记的字符串
        """
        # 获取对应颜色和样式
        color, style = self.COLOR_MAP.get(level.upper(), ("white", ""))
        # 构造带样式的日志格式：级别列8字符左对齐，竖线分隔符，消息内容继承颜色[6](@ref)
        return f"[{style} {color}]{level.upper():<8}│[/] [{color}]{message}[/]"


class Haha:
    def __init__(self, total: Optional[int] = None, desc: str = "Processing",
                 log_lines: int = 3, refresh_interval: float = 0.3):
        """线程安全的进度条控制器[3](@ref)
        参数:
            total: 总任务数
            desc: 进度条描述
            log_lines: 保留的日志行数（未实现）
            refresh_interval: 刷新间隔（秒）
        """
        # Rich控制台实例
        self.console = Console()
        # 线程锁保证操作原子性[7](@ref)
        self.lock = Lock()
        # 日志消息队列（生产者-消费者模式）[5](@ref)
        self.log_queue = Queue()
        # 进度条刷新频率
        self.refresh_interval = refresh_interval
        # 最后刷新时间戳
        self.last_refresh = 0
        # 颜色日志处理器
        self.logger = ColorLogger()
        # 进度条描述文字
        self.desc = desc

        # 配置Rich进度条组件[1,7](@ref)
        self.progress = Progress(
            TextColumn("[bold cyan]{task.description}"),  # 粗体青色描述
            BarColumn(bar_width=40, complete_style="cyan1", pulse_style="white"),  # 进度条样式
            TextColumn("[已完成 [green]{task.completed}[/]]"),  # 绿色已完成计数[1](@ref)
            TextColumn("[未完成 [yellow]{task.remaining}[/]]"),  # 黄色剩余计数[1](@ref)
            TextColumn("[总数 [white]{task.total}[/]]"),  # 白色总任务数[1](@ref)
            "•",  # 分隔符
            TaskProgressColumn(),  # 任务进度（如 97/100）
            "•",  # 分隔符
            TextColumn("已用时间："),
            TimeElapsedColumn(),  # 已用时间
            "⏳ ",  # 时间图标
            TextColumn("剩余时间："),
            TimeRemainingColumn(),  # 剩余时间
            transient=True,  # 完成后自动隐藏
            auto_refresh=False,  # 禁用自动刷新
            console=self.console  # 绑定控制台
        )

        # 添加进度条任务
        self.task = self.progress.add_task(desc, total=total)
        # 启动日志监控线程
        self._start_log_monitor()

    def _start_log_monitor(self):
        """启动日志消费者线程[5](@ref)"""

        def log_consumer():
            """日志消息处理循环"""
            while True:
                message = self.log_queue.get()
                if message is None:  # 接收到终止信号
                    break
                with self.lock:  # 保证控制台输出的原子性
                    self.console.print(message)
                    self.progress.refresh()  # 刷新进度条显示

        # 创建并启动后台线程
        self.log_thread = threading.Thread(target=log_consumer, daemon=True)
        self.log_thread.start()

    def log(self, level: str, message: str):
        """记录分级日志[6](@ref)
        参数:
            level: 日志级别（INFO/ERROR等）
            message: 日志内容
        """
        colored_msg = self.logger._colorize(level, message)
        self.log_queue.put(colored_msg)  # 将消息放入队列

    def info(self, message: str):
        """记录INFO级别日志[6](@ref)"""
        colored_msg = self.logger._colorize("INFO", message)
        self.log_queue.put(colored_msg)

    def error(self, message: str):
        """记录ERROR级别日志[6](@ref)"""
        colored_msg = self.logger._colorize("ERROR", message)
        self.log_queue.put(colored_msg)

    def update(self, advance: int = 1, desc: Optional[str] = None):
        """更新进度状态[7](@ref)
        参数:
            advance: 进度推进值
            desc: 新的描述文字
        """
        with self.lock:  # 保证线程安全
            current_time = time.time()
            # 达到刷新间隔才执行完整更新
            if current_time - self.last_refresh >= self.refresh_interval:
                update_args = {"advance": advance}
                if desc:
                    update_args["description"] = desc
                # 执行带刷新的进度更新
                self.progress.update(self.task, **update_args, refresh=True)
                self.last_refresh = current_time
            else:
                # 仅推进进度不刷新显示
                self.progress.advance(self.task, advance)

    def __enter__(self):
        """上下文管理器入口：启动进度条"""
        self.progress.start()
        return self

    def __exit__(self, *args):
        """上下文管理器退出：清理资源"""
        self.log_queue.put(None)  # 发送终止信号
        self.log_thread.join()  # 等待日志线程结束
        self.progress.stop()  # 停止进度条
