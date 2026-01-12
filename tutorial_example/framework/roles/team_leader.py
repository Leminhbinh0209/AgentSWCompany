"""Team Leader role for orchestrating team workflow"""
from framework.role import Role
from framework.actions.write_prd import WritePRD
from framework.actions.write_design import WriteDesign
from framework.actions.write_code import WriteCode
from framework.schema import Message


class TeamLeader(Role):
    """Team Leader that orchestrates the team workflow"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="TeamLeader",
            profile="Team Leader",
            goal="Manage and coordinate the team to complete software projects",
            actions=[],  # TeamLeader coordinates, doesn't execute actions directly
            llm=llm
        )
    
    def _get_team_info(self) -> str:
        """Get information about team members"""
        if not hasattr(self, '_environment') or not self._environment:
            return ""
        
        team_info = ""
        for role in self._environment.roles.values():
            if role.name != "TeamLeader":
                team_info += f"{role.name}: {role.profile}, {role.goal}\n"
        return team_info
    
    def publish_team_message(self, content: str, send_to: str = ""):
        """
        Publish a message to the team
        
        Args:
            content: Message content
            send_to: Target role (empty = broadcast)
        """
        if hasattr(self, '_environment') and self._environment:
            message = Message(
                content=content,
                role=self.name,
                cause_by="TeamLeader",
                send_to=send_to if send_to else None
            )
            self._environment.publish_message(message, send_to=send_to if send_to else None)
    
    async def react(self):
        """
        TeamLeader coordinates the team
        
        Returns:
            Coordination message or None
        """
        # TeamLeader observes team state and coordinates
        # In a simple implementation, it just passes through
        # In a more sophisticated version, it would analyze team state
        # and make coordination decisions
        
        if not hasattr(self, '_environment') or not self._environment:
            return None
        
        team_info = self._get_team_info()
        if team_info:
            coordination_msg = f"Team coordination: {len(self._environment.roles)} roles active"
            return Message(
                content=coordination_msg,
                role=self.name,
                cause_by="TeamLeader"
            )
        return None

