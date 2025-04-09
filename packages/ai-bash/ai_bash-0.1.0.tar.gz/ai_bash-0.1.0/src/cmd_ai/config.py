"""
配置管理模块
"""

import os
from typing import Dict, Optional

from dotenv import load_dotenv


class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置管理器"""
        self.config_loaded = False
        self.config_file = os.path.expanduser("~/.cmd_ai")
        self.env_vars = {}
    
    def load_config(self) -> Dict[str, str]:
        """
        加载配置文件
        
        Returns:
            包含配置项的字典
        """
        if self.config_loaded:
            return self.env_vars
        
        # 首先尝试加载项目根目录的.env文件
        load_dotenv()
        
        # 然后尝试加载用户主目录的.cmd_ai文件
        if os.path.exists(self.config_file):
            load_dotenv(self.config_file)
        
        # 获取所有相关环境变量
        self.env_vars = {
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
            "OPENAI_API_HOST": os.environ.get("OPENAI_API_HOST"),
            "OPENAI_MODEL_NAME": os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        }
        
        self.config_loaded = True
        return self.env_vars
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取配置项值
        
        Args:
            key: 配置项键名
            default: 默认值
            
        Returns:
            配置项的值,如果不存在则返回默认值
        """
        if not self.config_loaded:
            self.load_config()
        return self.env_vars.get(key, default)
    
    def is_configured(self) -> bool:
        """
        检查是否已经配置了必要的配置项
        
        Returns:
            是否配置完成
        """
        return bool(self.get("OPENAI_API_KEY")) 