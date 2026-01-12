"""Role implementations"""
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.roles.qa_engineer import QAEngineer
from framework.roles.technical_writer import TechnicalWriter
from framework.roles.devops_engineer import DevOpsEngineer
from framework.roles.team_leader import TeamLeader

__all__ = [
    "ProductManager", "Architect", "Engineer",
    "QAEngineer", "TechnicalWriter", "DevOpsEngineer",
    "TeamLeader"
]

