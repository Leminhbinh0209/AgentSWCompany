"""Custom exceptions for the framework"""


class NoMoneyException(Exception):
    """Raised when budget is exceeded"""
    
    def __init__(self, total_cost: float, message: str = ""):
        self.total_cost = total_cost
        super().__init__(message or f"Budget exceeded: ${total_cost:.2f}")

