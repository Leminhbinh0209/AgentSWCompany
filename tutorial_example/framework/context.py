"""Context for managing project state, configuration, and costs"""
from typing import Any, Dict, Optional
from pathlib import Path
from framework.utils.cost_manager import CostManager


class AttrDict:
    """A dict-like object that allows access to keys as attributes"""
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __getattr__(self, key):
        return self.__dict__.get(key, None)
    
    def __setattr__(self, key, value):
        self.__dict__[key] = value
    
    def __delattr__(self, key):
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise AttributeError(f"No such attribute: {key}")
    
    def get(self, key, default: Any = None):
        """Get value with default"""
        return self.__dict__.get(key, default)
    
    def set(self, key, val: Any):
        """Set value"""
        self.__dict__[key] = val
    
    def remove(self, key):
        """Remove key"""
        if key in self.__dict__:
            del self.__dict__[key]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.__dict__.copy()
    
    def update(self, other: Dict[str, Any]):
        """Update from dictionary"""
        self.__dict__.update(other)


class Context:
    """Environment context for managing project state, config, and costs"""
    
    def __init__(self, config=None):
        """
        Initialize Context
        
        Args:
            config: Optional configuration object
        """
        self.kwargs = AttrDict()  # Stores project_path, etc.
        self.config = config  # Configuration object
        self.cost_manager = CostManager()
    
    def set_project_path(self, path: str):
        """Set and create project path"""
        self.kwargs.project_path = path
        Path(path).mkdir(parents=True, exist_ok=True)
    
    def get_project_path(self) -> Optional[str]:
        """Get project path"""
        return self.kwargs.get("project_path")
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize context to dictionary"""
        return {
            "kwargs": self.kwargs.to_dict(),
            "cost_manager": {
                "total_cost": self.cost_manager.total_cost,
                "max_budget": self.cost_manager.max_budget,
            }
        }
    
    def deserialize(self, data: Dict[str, Any]):
        """Deserialize context from dictionary"""
        if "kwargs" in data:
            self.kwargs.update(data["kwargs"])
        if "cost_manager" in data:
            cm_data = data["cost_manager"]
            self.cost_manager.total_cost = cm_data.get("total_cost", 0.0)
            self.cost_manager.max_budget = cm_data.get("max_budget", 0.0)

