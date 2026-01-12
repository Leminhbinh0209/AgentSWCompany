"""Architect role"""
from framework.role import Role
from framework.actions.write_design import WriteDesign


class Architect(Role):
    """System Architect role"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Architect",
            profile="System Architect",
            goal="Create system designs based on PRDs",
            actions=[WriteDesign(llm=llm)],
            llm=llm
        )

