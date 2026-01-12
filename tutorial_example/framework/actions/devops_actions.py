"""Actions for DevOps tasks"""
from typing import List
from framework.action import Action
from framework.schema import Message, ActionOutput


class CreateDockerfile(Action):
    """Action to create Dockerfile"""
    
    def __init__(self, llm=None):
        super().__init__(name="CreateDockerfile", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate Dockerfile"""
        project_info = ""
        if messages:
            project_info = messages[-1].content
        
        system_prompt = """You are a DevOps Engineer. Create optimized Dockerfiles following best practices."""
        
        prompt = f"""Create a Dockerfile for a Python project based on:

{project_info}

Requirements:
1. Use appropriate Python base image
2. Set working directory
3. Copy requirements and install dependencies
4. Copy application code
5. Expose necessary ports
6. Set entrypoint
7. Follow best practices (multi-stage if needed)
"""
        
        dockerfile = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=dockerfile,
            instruct_content={"type": "dockerfile", "content": dockerfile}
        )


class SetupCI(Action):
    """Action to setup CI/CD configuration"""
    
    def __init__(self, llm=None):
        super().__init__(name="SetupCI", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate CI/CD configuration"""
        project_info = ""
        if messages:
            project_info = messages[-1].content
        
        ci_type = kwargs.get("ci_type", "github_actions")
        
        system_prompt = f"""You are a DevOps Engineer. Create {ci_type} CI/CD configuration."""
        
        if ci_type == "github_actions":
            prompt = f"""Create GitHub Actions workflow for:

{project_info}

Include:
1. Trigger on push/PR
2. Setup Python
3. Install dependencies
4. Run tests
5. Build (if applicable)
6. Deploy (optional)
"""
        else:
            prompt = f"""Create CI/CD configuration ({ci_type}) for:

{project_info}
"""
        
        ci_config = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=ci_config,
            instruct_content={"type": "ci_config", "ci_type": ci_type}
        )


class CreateDeployScript(Action):
    """Action to create deployment scripts"""
    
    def __init__(self, llm=None):
        super().__init__(name="CreateDeployScript", llm=llm)
    
    async def run(self, messages: List[Message] = None, **kwargs) -> ActionOutput:
        """Generate deployment script"""
        project_info = ""
        if messages:
            project_info = messages[-1].content
        
        deploy_type = kwargs.get("deploy_type", "bash")
        
        system_prompt = """You are a DevOps Engineer. Create deployment scripts that are 
        safe, idempotent, and include error handling."""
        
        prompt = f"""Create a {deploy_type} deployment script for:

{project_info}

Include:
1. Environment checks
2. Dependency installation
3. Build steps
4. Deployment steps
5. Health checks
6. Rollback capability (if applicable)
7. Error handling
"""
        
        deploy_script = await self._ask_llm(prompt, system_prompt)
        
        return ActionOutput(
            content=deploy_script,
            instruct_content={"type": "deploy_script", "deploy_type": deploy_type}
        )

