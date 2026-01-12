"""Product Manager role"""
from framework.role import Role
from framework.actions.write_prd import WritePRD


class ProductManager(Role):
    """Product Manager role"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="ProductManager",
            profile="Product Manager",
            goal="Create comprehensive PRDs based on requirements",
            actions=[WritePRD(llm=llm)],
            llm=llm
        )

