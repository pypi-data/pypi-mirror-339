"""
大模型API调用模块
"""

import os
import platform
import sys
from typing import Dict, Optional

from openai import OpenAI


class LLMClient:
    """大模型客户端类"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_host: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        """
        初始化大模型客户端

        Args:
            api_key: OpenAI API密钥,如果为None则从环境变量获取
            api_host: OpenAI API主机地址,如果为None则使用默认地址
            model_name: 使用的模型名称,如果为None则使用默认模型
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到OpenAI API密钥。请设置OPENAI_API_KEY环境变量或在初始化时提供。"
            )

        self.api_host = api_host or os.environ.get("OPENAI_API_HOST")
        self.model_name = model_name or os.environ.get(
            "OPENAI_MODEL_NAME", "gpt-3.5-turbo"
        )

        # 初始化客户端
        client_kwargs = {"api_key": self.api_key}
        if self.api_host:
            client_kwargs["base_url"] = self.api_host

        self.client = OpenAI(**client_kwargs)
        self.system_info = self._get_system_info()

    def _get_system_info(self) -> Dict[str, str]:
        """
        获取当前系统信息

        Returns:
            包含系统信息的字典
        """
        system_info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "platform": sys.platform,
        }

        # 检测具体的命令行环境
        if system_info["os"] == "Windows":
            # 检测是否运行在PowerShell、CMD或WSL中
            if "PROMPT" in os.environ and "$P$G" in os.environ.get("PROMPT", ""):
                system_info["shell"] = "cmd"
            elif "WT_SESSION" in os.environ or "TERM_PROGRAM" in os.environ:
                system_info["shell"] = "powershell"
            else:
                system_info["shell"] = "cmd"  # 默认假设是CMD
        else:
            # Unix-like系统检测当前shell
            shell_path = os.environ.get("SHELL", "")
            if shell_path:
                shell_name = os.path.basename(shell_path)
                system_info["shell"] = shell_name
            else:
                system_info["shell"] = "bash"  # 默认假设是bash

        # 如果在WSL中运行
        if "WSL_DISTRO_NAME" in os.environ:
            system_info["wsl"] = os.environ["WSL_DISTRO_NAME"]

        return system_info

    def generate_command(self, user_query: str) -> str:
        """
        根据用户查询生成命令行命令

        Args:
            user_query: 用户的自然语言查询

        Returns:
            生成的命令行命令
        """
        # 构建详细的系统信息提示
        os_info = f"操作系统: {self.system_info['os']}"
        if self.system_info["os"] == "Windows":
            os_info += f" (版本: {self.system_info['os_version']})"
            shell_info = f"命令行环境: {self.system_info['shell']}"
        elif self.system_info["os"] == "Linux":
            if "wsl" in self.system_info:
                os_info += f" (WSL: {self.system_info['wsl']})"
            else:
                os_info += f" (发行版: {self.system_info['os_release']})"
            shell_info = f"Shell: {self.system_info['shell']}"
        elif self.system_info["os"] == "Darwin":
            os_info += f" (macOS 版本: {self.system_info['os_version']})"
            shell_info = f"Shell: {self.system_info['shell']}"
        else:
            shell_info = f"命令行环境: {self.system_info.get('shell', '未知')}"

        system_prompt = f"""
        你是一个命令行专家助手。你的任务是将用户的自然语言需求转换为可在命令行中执行的命令。
        
        请严格根据以下系统环境信息生成命令:
        - {os_info}
        - {shell_info}
        - 系统架构: {self.system_info["architecture"]}
        
        考虑用户当前的操作系统和Shell环境,生成最适合该环境的命令。例如:
        - 在Windows CMD中使用dir而不是ls
        - 在Windows PowerShell中可以使用ls或Get-ChildItem
        - 在Linux/macOS中使用ls而不是dir
        
        只返回可执行的命令,不要包含其他解释或标记。如果需要多个命令,根据用户的Shell类型使用适当的分隔符(例如Windows上的&&,Unix-like系统上的;或&&)。
        如果无法确定合适的命令,请回复"无法生成对应的命令"。
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                max_tokens=100,
                temperature=0.0,
            )

            command = response.choices[0].message.content.strip()
            return command
        except Exception as e:
            raise RuntimeError(f"调用大模型API时发生错误: {str(e)}")
