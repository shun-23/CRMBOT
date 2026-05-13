"""
核心配置模块 - 管理所有环境变量和配置项

重构更新：
- embedding_model 改为 bge-m3 (BAAI 中英双语嵌入模型)
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类，自动从环境变量加载"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # 应用基础配置
    app_name: str = Field(default="智能销售 AI Agent", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")
    
    # API 配置
    api_v1_prefix: str = Field(default="/api/v1", description="API 版本前缀")
    host: str = Field(default="0.0.0.0", description="服务监听地址")
    port: int = Field(default=8000, description="服务端口")
    
    # CORS 配置
    cors_origins: List[str] = Field(
        default=["*"],
        description="允许的跨域来源（微信小程序需要配置域名）"
    )
    
    # LLM 配置（DeepSeek V4 Flash）
    openai_api_key: Optional[str] = Field(default=None, description="DeepSeek API Key")
    openai_base_url: Optional[str] = Field(
        default="https://api.deepseek.com/v1",
        description="DeepSeek API Base URL"
    )
    default_model: str = Field(default="deepseek-v4-pro", description="默认使用的模型 (deepseek-v4-flash | deepseek-v4-pro)")
    
    # Embedding 配置（Ollama）
    embedding_model: str = Field(
        default="bge-m3",
        description="Ollama 向量化模型 (BAAI BGE-M3 中英双语)"
    )
    
    # LangGraph 配置
    max_iterations: int = Field(default=10, description="最大迭代次数，防止死循环")
    
    # PostgreSQL 数据库配置（持久化）
    database_url: Optional[str] = Field(
        default=None,
        description="PostgreSQL 连接字符串（用于 LangGraph 状态持久化）"
    )
    
    # 知识库配置
    knowledge_base_path: str = Field(
        default="./data/knowledge_base",
        description="知识库文件存储路径"
    )
    vector_store_path: str = Field(
        default="./data/vector_store",
        description="向量数据库存储路径"
    )
    
    # 文档生成配置
    output_dir: str = Field(
        default="./output",
        description="生成文档的输出目录"
    )
    
    # 项目根目录
    base_dir: str = Field(
        default=".",
        description="项目根目录"
    )
    
    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式"
    )


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例（缓存以提高性能）"""
    return Settings()


# 全局配置实例
settings = get_settings()
