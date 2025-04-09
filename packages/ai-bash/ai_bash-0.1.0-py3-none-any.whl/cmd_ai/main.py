"""
命令行工具主模块
"""

import subprocess
import sys
from typing import Optional

import click

from cmd_ai.config import Config
from cmd_ai.llm import LLMClient


@click.command()
@click.argument("query", required=False)
@click.option(
    "--api-key", "-k", help="OpenAI API密钥,如果不提供则从配置文件或环境变量中读取"
)
@click.option(
    "--api-host", "-h", help="OpenAI API主机地址,如果不提供则从配置文件或环境变量中读取"
)
@click.option("--model", "-m", help="使用的模型名称,默认为gpt-3.5-turbo或从配置中读取")
@click.option("--no-exec", "-n", is_flag=True, help="只输出命令而不执行")
@click.option("--verbose", "-v", is_flag=True, help="显示详细的系统信息")
def main(
    query: Optional[str],
    api_key: Optional[str],
    api_host: Optional[str],
    model: Optional[str],
    no_exec: bool,
    verbose: bool,
):
    """
    将自然语言需求转换为命令行命令。

    如果不提供查询参数,将提示用户输入。
    """
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

    # 如果没有提供查询参数,提示用户输入
    if not query:
        query = click.prompt("请输入你的需求", type=str)

    try:
        command = llm_client.generate_command(query)

        if command == "无法生成对应的命令":
            click.echo("无法为您的需求生成合适的命令")
            sys.exit(1)

        # 输出生成的命令
        click.echo(f"生成的命令: {command}")

        # 如果指定了--no-exec选项，则只输出不执行
        if no_exec:
            return

        # 等待用户确认后执行
        click.echo("按回车键执行命令...", nl=False)
        input()

        # 执行命令
        click.echo(f"\n正在执行: {command}")
        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)

    except Exception as e:
        click.echo(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
