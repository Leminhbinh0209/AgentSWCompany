"""Team orchestration"""
from typing import List, Optional
from pathlib import Path
import json
from framework.role import Role
from framework.environment import Environment
from framework.schema import Message
from framework.context import Context
from framework.config import Config
from framework.utils.exceptions import NoMoneyException


class Team:
    """Team that manages multiple roles"""
    
    def __init__(self, context: Optional[Context] = None):
        """
        Initialize Team
        
        Args:
            context: Optional context object
        """
        self.context = context or Context()
        self.environment = Environment(context=self.context)
        self.idea: str = ""
        self.investment: float = 0.0
        self.max_rounds: int = 10
        self.current_round: int = 0
    
    def hire(self, roles: List[Role]):
        """Hire roles to the team"""
        self.environment.add_roles(roles)
    
    def invest(self, amount: float):
        """
        Invest in the company and set budget
        
        Args:
            amount: Investment amount
        """
        self.investment = amount
        self.context.cost_manager.max_budget = amount
    
    def _check_balance(self):
        """Check if budget is sufficient"""
        if self.context.cost_manager.total_cost >= self.context.cost_manager.max_budget:
            raise NoMoneyException(
                self.context.cost_manager.total_cost,
                f"Insufficient funds: ${self.context.cost_manager.total_cost:.2f} >= ${self.context.cost_manager.max_budget:.2f}"
            )
    
    def run_project(self, idea: str, send_to: str = ""):
        """
        Run a project from publishing user requirement
        
        Args:
            idea: Project idea
            send_to: Target role (default: ProductManager)
        """
        self.idea = idea
        initial_message = Message(
            content=idea,
            role="User",
            cause_by="UserRequirement"
        )
        target = send_to or "ProductManager"
        self.environment.publish_message(initial_message, send_to=target)
    
    async def run(self, n_round: int = 10, idea: str = "", send_to: str = "", auto_archive: bool = True):
        """
        Run company until target round or no money
        
        Args:
            n_round: Number of rounds to run
            idea: Project idea (if provided, calls run_project)
            send_to: Target role for initial message
            auto_archive: Whether to archive after completion
            
        Returns:
            Message history
        """
        if idea:
            self.run_project(idea=idea, send_to=send_to)
        
        self.max_rounds = n_round
        self.current_round = 0
        
        while n_round > 0:
            if self.environment.is_idle:
                break
            
            self.current_round = self.max_rounds - n_round
            print(f"\n{'='*60}")
            print(f"Round {self.current_round + 1}/{self.max_rounds}")
            print(f"{'='*60}")
            
            # Check budget
            self._check_balance()
            
            # Run environment (processes all roles)
            await self.environment.run()
            
            # Check if complete
            if self._is_complete():
                print("\n✓ Task completed!")
                break
            
            n_round -= 1
        
        # Archive project
        self.environment.archive(auto_archive)
        
        # Return context (backward compatibility)
        if isinstance(self.environment.context, dict):
            return self.environment.context
        else:
            # Convert Context to dict for backward compatibility
            result = self.environment.context.kwargs.to_dict()
            # Ensure prd, design, code are in result
            if "prd" not in result:
                result["prd"] = self.environment.context.kwargs.get("prd", "")
            if "design" not in result:
                result["design"] = self.environment.context.kwargs.get("design", "")
            if "code" not in result:
                result["code"] = self.environment.context.kwargs.get("code", "")
            return result
    
    def _route_message(self, message: Message, process_next_round: bool = False):
        """Route message to appropriate role based on cause_by"""
        # Simple routing logic
        routing_map = {
            "WritePRD": "Architect",  # PRD goes to Architect
            "WriteDesign": "Engineer",  # Design goes to Engineer
            "WriteCode": None,  # Code is final output
        }
        
        target_role = routing_map.get(message.cause_by)
        if target_role:
            # Send to specific role
            self.environment.publish_message(message, send_to=target_role)
        else:
            # Final output - store in context
            if message.cause_by == "WriteCode":
                self.environment.context["code"] = message.content
                self.environment.context["design"] = self._find_latest_message("WriteDesign")
                self.environment.context["prd"] = self._find_latest_message("WritePRD")
    
    def _find_latest_message(self, cause_by: str) -> str:
        """Find latest message with given cause_by"""
        for msg in reversed(self.environment.message_history):
            if msg.cause_by == cause_by:
                return msg.content
        return ""
    
    def _is_complete(self) -> bool:
        """Check if task is complete"""
        if isinstance(self.environment.context, dict):
            return "code" in self.environment.context
        else:
            return "code" in self.environment.context.kwargs.to_dict()
    
    def serialize(self, stg_path: Optional[Path] = None):
        """
        Serialize team state to disk
        
        Args:
            stg_path: Storage path (default: ./storage/team)
        """
        if stg_path is None:
            stg_path = Path("./storage/team")
        
        stg_path.mkdir(parents=True, exist_ok=True)
        team_info_path = stg_path / "team.json"
        
        serialized_data = {
            "idea": self.idea,
            "investment": self.investment,
            "current_round": self.current_round,
            "max_rounds": self.max_rounds,
            "roles": [role.name for role in self.environment.roles.values()],
            "context": self.context.serialize(),
        }
        
        with open(team_info_path, 'w') as f:
            json.dump(serialized_data, f, indent=2, default=str)
    
    @classmethod
    def deserialize(cls, stg_path: Path, context: Optional[Context] = None):
        """
        Deserialize team state from disk
        
        Args:
            stg_path: Storage path
            context: Optional context object
            
        Returns:
            Team instance
        """
        team_info_path = stg_path / "team.json"
        if not team_info_path.exists():
            raise FileNotFoundError(f"Team file not found: {team_info_path}")
        
        with open(team_info_path, 'r') as f:
            team_info = json.load(f)
        
        ctx = context or Context()
        ctx.deserialize(team_info.pop("context", {}))
        
        team = cls(context=ctx)
        team.idea = team_info.get("idea", "")
        team.investment = team_info.get("investment", 0.0)
        team.current_round = team_info.get("current_round", 0)
        team.max_rounds = team_info.get("max_rounds", 10)
        
        return team
    
    @property
    def cost_manager(self):
        """Get cost manager"""
        return self.context.cost_manager

