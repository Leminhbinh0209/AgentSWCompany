"""Configuration management"""
from typing import Optional, Dict, Any
from pathlib import Path
import yaml


class LLMConfig:
    """LLM configuration"""
    
    def __init__(
        self,
        api_type: str = "vllm",
        base_url: str = "http://localhost:8000/v1",
        api_key: str = "",
        model: str = "codellama/CodeLlama-7b-Instruct-hf",
        local_model_path: str = "EMPTY"
    ):
        self.api_type = api_type
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.local_model_path = local_model_path


class Config:
    """Centralized configuration"""
    
    def __init__(self):
        self.llm = LLMConfig()
        self.project_path = ""
        self.workspace = "workspace"
        self.repair_llm_output = True
    
    @classmethod
    def default(cls):
        """Create default configuration"""
        return cls()
    
    @classmethod
    def from_yaml(cls, path: str):
        """Load configuration from YAML file"""
        config = cls()
        
        if not Path(path).exists():
            return config
        
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        if "llm" in data:
            llm_data = data["llm"]
            config.llm = LLMConfig(
                api_type=llm_data.get("api_type", "vllm"),
                base_url=llm_data.get("base_url", "http://localhost:8000/v1"),
                api_key=llm_data.get("api_key", ""),
                model=llm_data.get("model", "codellama/CodeLlama-7b-Instruct-hf"),
                local_model_path=llm_data.get("local_model_path", "EMPTY")
            )
        
        if "workspace" in data:
            config.workspace = data["workspace"]
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "llm": {
                "api_type": self.llm.api_type,
                "base_url": self.llm.base_url,
                "api_key": self.llm.api_key,
                "model": self.llm.model,
                "local_model_path": self.llm.local_model_path,
            },
            "workspace": self.workspace,
            "repair_llm_output": self.repair_llm_output
        }

