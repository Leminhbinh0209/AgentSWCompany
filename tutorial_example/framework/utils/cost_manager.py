"""Cost Manager for tracking API costs and budget"""
from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CostRecord:
    """Record of a single cost transaction"""
    timestamp: datetime
    role: str
    action: str
    cost: float
    description: str = ""


class CostManager:
    """Manages API costs and budget enforcement"""
    
    def __init__(self, max_budget: float = 0.0):
        """
        Initialize Cost Manager
        
        Args:
            max_budget: Maximum budget allowed
        """
        self.total_cost: float = 0.0
        self.max_budget: float = max_budget
        self.cost_history: List[CostRecord] = []
    
    def add_cost(self, cost: float, role: str = "", action: str = "", description: str = ""):
        """
        Add a cost and check budget
        
        Args:
            cost: Cost amount
            role: Role that incurred the cost
            action: Action that incurred the cost
            description: Description of the cost
            
        Raises:
            NoMoneyException: If budget is exceeded
        """
        self.total_cost += cost
        
        record = CostRecord(
            timestamp=datetime.now(),
            role=role,
            action=action,
            cost=cost,
            description=description
        )
        self.cost_history.append(record)
        
        # Check budget
        if self.max_budget > 0 and self.total_cost >= self.max_budget:
            from framework.utils.exceptions import NoMoneyException
            raise NoMoneyException(
                self.total_cost,
                f"Insufficient funds: ${self.total_cost:.2f} >= ${self.max_budget:.2f}"
            )
    
    def get_remaining_budget(self) -> float:
        """Get remaining budget"""
        if self.max_budget <= 0:
            return float('inf')
        return max(0.0, self.max_budget - self.total_cost)
    
    def reset(self):
        """Reset cost tracking"""
        self.total_cost = 0.0
        self.cost_history.clear()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get cost summary"""
        return {
            "total_cost": self.total_cost,
            "max_budget": self.max_budget,
            "remaining": self.get_remaining_budget(),
            "transactions": len(self.cost_history)
        }

