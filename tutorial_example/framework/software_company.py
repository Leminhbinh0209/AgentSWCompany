"""Software Company - Main entry point for automated project generation"""
import asyncio
from pathlib import Path
from typing import Optional
from framework.team import Team
from framework.context import Context
from framework.config import Config
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.roles.team_leader import TeamLeader
from framework.llm import get_llm


def generate_repo(
    idea: str,
    investment: float = 10.0,
    n_round: int = 8,
    project_name: str = "",
    project_path: str = "",
    recover_path: Optional[str] = None,
    llm=None
):
    """
    Generate a complete project repository - fully automated.
    
    Similar to MetaGPT's generate_repo function.
    
    Args:
        idea: Project idea/requirement
        investment: Budget for the project
        n_round: Number of workflow rounds
        project_name: Optional project name
        project_path: Optional project path
        recover_path: Optional path to recover from saved state
        llm: Optional LLM instance
        
    Returns:
        Project path
    """
    # Initialize LLM if not provided
    if llm is None:
        llm = get_llm(
            local_model_path="EMPTY",
            vllm_base_url="http://localhost:8000/v1",
            vllm_model="codellama/CodeLlama-7b-Instruct-hf"
        )
    
    # Create context
    config = Config.default()
    ctx = Context(config=config)
    
    # Set project path
    if project_path:
        ctx.set_project_path(project_path)
    elif project_name:
        workspace = config.workspace
        project_path = f"{workspace}/{project_name}"
        ctx.set_project_path(project_path)
    
    # Recover or create new team
    if recover_path:
        stg_path = Path(recover_path)
        if not stg_path.exists() or not str(stg_path).endswith("team"):
            raise FileNotFoundError(f"{recover_path} not exists or not endswith `team`")
        company = Team.deserialize(stg_path=stg_path, context=ctx)
        idea = company.idea
    else:
        # Create new team
        company = Team(context=ctx)
        company.hire([
            TeamLeader(llm=llm),
            ProductManager(llm=llm),
            Architect(llm=llm),
            Engineer(llm=llm),
        ])
    
    # Invest and run
    company.invest(investment)
    asyncio.run(company.run(n_round=n_round, idea=idea))
    
    # Return project path
    return ctx.get_project_path() or project_path or config.workspace


async def generate_repo_async(
    idea: str,
    investment: float = 10.0,
    n_round: int = 8,
    project_name: str = "",
    project_path: str = "",
    recover_path: Optional[str] = None,
    llm=None
):
    """
    Async version of generate_repo
    
    Args:
        idea: Project idea/requirement
        investment: Budget for the project
        n_round: Number of workflow rounds
        project_name: Optional project name
        project_path: Optional project path
        recover_path: Optional path to recover from saved state
        llm: Optional LLM instance
        
    Returns:
        Project path
    """
    # Initialize LLM if not provided
    if llm is None:
        llm = get_llm(
            local_model_path="EMPTY",
            vllm_base_url="http://localhost:8000/v1",
            vllm_model="codellama/CodeLlama-7b-Instruct-hf"
        )
    
    # Create context
    config = Config.default()
    ctx = Context(config=config)
    
    # Set project path
    if project_path:
        ctx.set_project_path(project_path)
    elif project_name:
        workspace = config.workspace
        project_path = f"{workspace}/{project_name}"
        ctx.set_project_path(project_path)
    
    # Recover or create new team
    if recover_path:
        stg_path = Path(recover_path)
        if not stg_path.exists() or not str(stg_path).endswith("team"):
            raise FileNotFoundError(f"{recover_path} not exists or not endswith `team`")
        company = Team.deserialize(stg_path=stg_path, context=ctx)
        idea = company.idea
    else:
        # Create new team
        company = Team(context=ctx)
        company.hire([
            TeamLeader(llm=llm),
            ProductManager(llm=llm),
            Architect(llm=llm),
            Engineer(llm=llm),
        ])
    
    # Invest and run
    company.invest(investment)
    await company.run(n_round=n_round, idea=idea)
    
    # Return project path
    return ctx.get_project_path() or project_path or config.workspace

