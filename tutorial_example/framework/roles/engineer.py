"""Engineer role"""
from framework.role import Role
from framework.actions.write_code import WriteCode


class Engineer(Role):
    """Software Engineer role"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Engineer",
            profile="Software Engineer",
            goal="Write clean, functional code based on designs",
            actions=[WriteCode(llm=llm)],
            llm=llm
        )

