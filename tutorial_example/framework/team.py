"""Team orchestration"""
from typing import List
from framework.role import Role
from framework.environment import Environment
from framework.schema import Message


class Team:
    """Team that manages multiple roles"""
    
    def __init__(self):
        self.environment = Environment()
        self.idea: str = ""
        self.investment: float = 0.0
        self.max_rounds: int = 10
        self.current_round: int = 0
    
    def hire(self, roles: List[Role]):
        """Hire roles to the team"""
        self.environment.add_roles(roles)
    
    def invest(self, amount: float):
        """Set investment/budget"""
        self.investment = amount
    
    async def run(self, idea: str, n_round: int = 10):
        """
        Run the team simulation
        
        Args:
            idea: The initial idea/requirement
            n_round: Number of rounds to run
        """
        self.idea = idea
        self.max_rounds = n_round
        self.current_round = 0
        
        # Initialize with the idea - send only to ProductManager
        initial_message = Message(
            content=idea,
            role="User",
            cause_by="UserRequirement"
        )
        self.environment.publish_message(initial_message, send_to="ProductManager")
        
        # Run rounds - process roles in sequence
        for round_num in range(n_round):
            self.current_round = round_num
            print(f"\n{'='*60}")
            print(f"Round {round_num + 1}/{n_round}")
            print(f"{'='*60}")
            
            # Process roles in order: ProductManager -> Architect -> Engineer
            role_order = ["ProductManager", "Architect", "Engineer"]
            messages_produced = []
            
            for role_name in role_order:
                role = self.environment.get_role(role_name)
                if not role:
                    continue
                
                # Only react if role has messages to process
                if role.working_memory:
                    message = await role.react()
                    if message:
                        print(f"\n[{role.name}] produced message:")
                        print(f"  Cause: {message.cause_by}")
                        print(f"  Content preview: {message.content[:150]}...")
                        messages_produced.append(message)
                        # Route message immediately so next role can process it
                        self._route_message(message)
            
            # Check if we're done
            if self._is_complete():
                print("\n✓ Task completed!")
                break
            
            if not messages_produced:
                print("No messages produced this round. Stopping.")
                break
        
        return self.environment.context
    
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
        # Simple check: if we have code in context, we're done
        return "code" in self.environment.context

