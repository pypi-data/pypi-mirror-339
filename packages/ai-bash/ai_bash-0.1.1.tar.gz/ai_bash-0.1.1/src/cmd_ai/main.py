"""
命令行工具主模块
"""

import os
import subprocess
import sys
import threading
import time
from typing import Optional

import click

from cmd_ai.config import Config
from cmd_ai.llm import LLMClient


def copy_to_clipboard(text):
    """
    将文本复制到系统剪贴板

    Args:
        text: 要复制的文本

    Returns:
        成功返回True，失败返回False
    """
    try:
        # 检测操作系统
        if sys.platform == "darwin":  # macOS
            process = subprocess.Popen(
                ["pbcopy"], stdin=subprocess.PIPE, close_fds=True
            )
            process.communicate(text.encode("utf-8"))
        elif sys.platform == "win32":  # Windows
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, close_fds=True)
            process.communicate(text.encode("utf-8"))
        else:  # Linux and other Unix-like
            # 尝试使用xclip（X11系统）
            try:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"],
                    stdin=subprocess.PIPE,
                    close_fds=True,
                )
                process.communicate(text.encode("utf-8"))
            except FileNotFoundError:
                # 尝试使用wl-copy（Wayland系统）
                try:
                    process = subprocess.Popen(
                        ["wl-copy"], stdin=subprocess.PIPE, close_fds=True
                    )
                    process.communicate(text.encode("utf-8"))
                except FileNotFoundError:
                    return False
        return True
    except Exception:
        return False


def init_config(force=False):
    """
    初始化配置文件

    Args:
        force: 是否强制创建(覆盖已有配置)

    Returns:
        配置文件路径和是否新创建
    """
    config_obj = Config()
    config_path = config_obj.config_file

    click.echo(f"配置文件路径: {config_path}")

    # 检查配置文件是否存在
    if os.path.exists(config_path) and not force:
        click.echo("配置文件已存在。如需重置,请使用 --init --force 选项。")
        return config_path, False

    # 创建新配置文件
    default_config = """# AI-Bash 配置文件

# 必需的API密钥 (必须设置此项)
OPENAI_API_KEY=你的OpenAI API密钥

# 可选的API主机地址 (用于私有部署或国内镜像站)
# OPENAI_API_HOST=https://your-api-host.com/v1

# 可选的模型名称 (默认为gpt-3.5-turbo)
# OPENAI_MODEL_NAME=gpt-4
"""
    # 确保目录存在
    os.makedirs(os.path.dirname(config_path) or ".", exist_ok=True)

    # 写入文件
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(default_config)

    click.echo(f"已创建默认配置文件: {config_path}")
    click.echo("请编辑此文件并设置您的OpenAI API密钥。")

    return config_path, True


class Spinner:
    """命令行加载动画效果类"""

    def __init__(self, message="加载中", delay=0.1):
        """
        初始化加载动画

        Args:
            message: 提示信息
            delay: 帧切换延迟时间,单位秒
        """
        self.message = message
        self.delay = delay
        self.spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        self.running = False
        self.spinner_thread = None

    def spin(self):
        """动画循环方法"""
        i = 0
        while self.running:
            char = self.spinner_chars[i % len(self.spinner_chars)]
            sys.stdout.write(f"\r{char} {self.message}...")
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1

    def start(self):
        """开始显示加载动画"""
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.daemon = True
        self.spinner_thread.start()

    def stop(self):
        """停止加载动画"""
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()


@click.command(context_settings=dict(ignore_unknown_options=False))
@click.argument("query", required=False, nargs=-1)
@click.option(
    "--api-key", "-k", help="OpenAI API密钥,如果不提供则从配置文件或环境变量中读取"
)
@click.option(
    "--api-host", "-h", help="OpenAI API主机地址,如果不提供则从配置文件或环境变量中读取"
)
@click.option("--model", "-m", help="使用的模型名称,默认为gpt-3.5-turbo或从配置中读取")
@click.option("--no-exec", "-n", is_flag=True, help="只输出命令而不执行")
@click.option("--verbose", "-v", is_flag=True, help="显示详细的系统信息")
@click.option(
    "--copy",
    "-c",
    is_flag=True,
    help="仅输出可复制的命令,不执行,适合复制到其他终端使用",
)
@click.option(
    "--clipboard",
    "-b",
    is_flag=True,
    help="自动将生成的命令复制到系统剪贴板,便于直接粘贴使用",
)
@click.option(
    "--init",
    "-i",
    is_flag=True,
    help="初始化配置文件,显示配置路径,如果配置不存在则创建",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="与--init一起使用,强制创建新配置文件,即使已存在也会覆盖",
)
def cli(
    query,
    api_key: Optional[str],
    api_host: Optional[str],
    model: Optional[str],
    no_exec: bool,
    verbose: bool,
    copy: bool,
    clipboard: bool,
    init: bool,
    force: bool,
):
    """AI-Bash: 将自然语言需求转换为命令行命令的工具

    直接输入查询内容（不需要引号）：

        ai 查一下当前目录的文件路径

        ai 列出所有进程 --no-exec

    初始化配置：

        ai --init           显示并根据需要创建配置
        ai --init --force   强制创建新配置文件

    命令选项：

        ai 查找大文件 --copy        仅输出纯文本命令
        ai 查找大文件 --clipboard   自动复制命令到剪贴板
    """
    # 处理初始化配置请求
    if init:
        config_path, created = init_config(force)
        if created:
            click.echo(f"可以使用您喜欢的编辑器修改配置文件: {config_path}")
            click.echo(f"例如: nano {config_path}")
            click.echo(f"     vi {config_path}")
            click.echo(f"     notepad {config_path} (Windows)")
        sys.exit(0)

    # 将参数列表合并为查询字符串
    query_str = " ".join(query) if query else None

    # 如果没有查询参数，显示帮助
    if not query_str:
        click.echo(cli.get_help(click.Context(cli)))
        sys.exit(0)

    # 加载配置
    config = Config()
    config.load_config()

    # 如果命令行参数没有提供各项配置,则从配置中获取
    api_key = api_key or config.get("OPENAI_API_KEY")
    api_host = api_host or config.get("OPENAI_API_HOST")
    model_name = model or config.get("OPENAI_MODEL_NAME")

    if not api_key:
        click.echo(
            "错误: 未找到OpenAI API密钥。请通过--api-key选项提供,或设置OPENAI_API_KEY环境变量。"
        )
        click.echo("提示: 使用 'ai --init' 可以创建并配置默认配置文件。")
        sys.exit(1)

    # 初始化大模型客户端
    try:
        llm_client = LLMClient(
            api_key=api_key, api_host=api_host, model_name=model_name
        )

        # 打印系统信息
        if verbose:
            system_info = llm_client.system_info
            click.echo("系统环境信息:")
            click.echo(f"- 操作系统: {system_info['os']}")
            if system_info["os"] == "Windows":
                click.echo(f"- 命令行: {system_info.get('shell', '未知')}")
            elif system_info["os"] == "Linux":
                if "wsl" in system_info:
                    click.echo(f"- WSL发行版: {system_info['wsl']}")
                click.echo(f"- Shell: {system_info.get('shell', '未知')}")
            elif system_info["os"] == "Darwin":
                click.echo(f"- Shell: {system_info.get('shell', '未知')}")
            click.echo(f"- 架构: {system_info['architecture']}")
            click.echo("-" * 50)

    except ValueError as e:
        click.echo(f"错误: {str(e)}")
        sys.exit(1)

    try:
        # 显示加载动画
        spinner = Spinner(message="正在生成命令")
        spinner.start()

        # 调用API生成命令
        command = llm_client.generate_command(query_str)

        # 停止加载动画
        spinner.stop()

        if command == "无法生成对应的命令":
            click.echo("无法为您的需求生成合适的命令")
            sys.exit(1)

        # 如果使用了--copy选项，则只输出命令本身便于复制
        if copy:
            click.echo(command)
            sys.exit(0)

        # 如果使用了--clipboard选项，自动复制到剪贴板
        if clipboard:
            copy_success = copy_to_clipboard(command)

            # 输出结果
            click.echo("\n命令:")
            click.secho(f"{command}", fg="green", bold=True)

            if copy_success:
                click.echo("\n✓ 已复制到剪贴板，可直接粘贴使用")
            else:
                click.echo("\n⚠️ 复制到剪贴板失败，请手动复制")

            sys.exit(0)

        # 输出生成的命令（使用颜色和换行使其更突出）

        click.secho(f"{command}", fg="green", bold=True)
        click.echo("")  # 额外的空行

        # 如果指定了--no-exec选项，则只输出不执行
        if no_exec:
            # 提供复制提示
            click.echo("提示: 使用 --clipboard 选项可自动复制命令到剪贴板")
            click.echo("     使用 --copy 选项可获取纯文本命令\n")
            return

        spinner = Spinner(message="按回车键执行命令，或按Ctrl+C取消...")
        spinner.start()
        # 等待用户确认后执行
        input()
        spinner.stop()
        # 执行命令

        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)

    except Exception as e:
        # 确保出错时停止加载动画
        try:
            spinner.stop()
        except:
            pass
        click.echo(f"错误: {str(e)}")
        sys.exit(1)


def main():
    """
    主函数,作为CLI入口点
    """
    try:
        cli()
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
