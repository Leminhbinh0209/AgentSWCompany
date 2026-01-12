"""Role implementations"""
from framework.roles.product_manager import ProductManager
from framework.roles.architect import Architect
from framework.roles.engineer import Engineer
from framework.roles.qa_engineer import QAEngineer
from framework.roles.technical_writer import TechnicalWriter
from framework.roles.devops_engineer import DevOpsEngineer

__all__ = [
    "ProductManager", "Architect", "Engineer",
    "QAEngineer", "TechnicalWriter", "DevOpsEngineer"
]

