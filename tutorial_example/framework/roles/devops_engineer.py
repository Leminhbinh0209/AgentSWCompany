"""DevOps Engineer role"""
from framework.role import Role
from framework.actions.devops_actions import CreateDockerfile, SetupCI, CreateDeployScript


class DevOpsEngineer(Role):
    """DevOps Engineer role for deployment and infrastructure"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="DevOpsEngineer",
            profile="DevOps Engineer",
            goal="Automate deployment, setup CI/CD, and manage infrastructure",
            actions=[CreateDockerfile(llm=llm), SetupCI(llm=llm), CreateDeployScript(llm=llm)],
            llm=llm
        )
    
    async def create_dockerfile(self, project_info: str) -> str:
        """
        Create Dockerfile
        
        Args:
            project_info: Project information
            
        Returns:
            Dockerfile content
        """
        from framework.schema import Message
        create_dockerfile_action = next((a for a in self.actions if isinstance(a, CreateDockerfile)), None)
        if create_dockerfile_action:
            messages = [Message(content=project_info, role="System", cause_by="DockerfileRequest")]
            result = await create_dockerfile_action.run(messages=messages)
            return result.content
        return ""
    
    async def setup_ci(self, project_info: str, ci_type: str = "github_actions") -> str:
        """
        Setup CI/CD
        
        Args:
            project_info: Project information
            ci_type: Type of CI (github_actions, gitlab_ci, etc.)
            
        Returns:
            CI configuration
        """
        from framework.schema import Message
        setup_ci_action = next((a for a in self.actions if isinstance(a, SetupCI)), None)
        if setup_ci_action:
            messages = [Message(content=project_info, role="System", cause_by="CIRequest")]
            result = await setup_ci_action.run(messages=messages, ci_type=ci_type)
            return result.content
        return ""
    
    async def create_deploy_script(self, project_info: str, deploy_type: str = "bash") -> str:
        """
        Create deployment script
        
        Args:
            project_info: Project information
            deploy_type: Type of script (bash, python, etc.)
            
        Returns:
            Deployment script
        """
        from framework.schema import Message
        create_deploy_action = next((a for a in self.actions if isinstance(a, CreateDeployScript)), None)
        if create_deploy_action:
            messages = [Message(content=project_info, role="System", cause_by="DeployScriptRequest")]
            result = await create_deploy_action.run(messages=messages, deploy_type=deploy_type)
            return result.content
        return ""

