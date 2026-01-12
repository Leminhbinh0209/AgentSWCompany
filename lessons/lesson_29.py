"""
Lesson 29: Cost Management
==========================

This lesson demonstrates the Cost Management system for tracking API costs
and enforcing budgets.

Run this lesson:
    python lesson_29.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.utils.cost_manager import CostManager, CostRecord
from framework.utils.exceptions import NoMoneyException


async def main():
    print("=" * 80)
    print("Lesson 29: Cost Management")
    print("=" * 80)
    print()
    
    print("Cost Management tracks API costs and enforces budget limits.")
    print("This prevents projects from exceeding their allocated budget.")
    print()
    
    # 1. Creating Cost Manager
    print("1. Creating Cost Manager")
    print("-" * 80)
    cost_mgr = CostManager(max_budget=10.0)
    print(f"✓ Cost Manager created")
    print(f"  - Initial budget: ${cost_mgr.max_budget:.2f}")
    print(f"  - Initial cost: ${cost_mgr.total_cost:.2f}")
    print()
    
    # 2. Adding Costs
    print("2. Adding Costs")
    print("-" * 80)
    cost_mgr.add_cost(0.5, role="ProductManager", action="WritePRD", description="PRD generation")
    cost_mgr.add_cost(0.3, role="Architect", action="WriteDesign", description="Design creation")
    cost_mgr.add_cost(0.4, role="Engineer", action="WriteCode", description="Code generation")
    
    print(f"✓ Costs added:")
    print(f"  - Total cost: ${cost_mgr.total_cost:.2f}")
    print(f"  - Transactions: {len(cost_mgr.cost_history)}")
    print()
    
    # 3. Cost History
    print("3. Cost History")
    print("-" * 80)
    print("Cost records:")
    for i, record in enumerate(cost_mgr.cost_history, 1):
        print(f"  {i}. [{record.role}] {record.action}: ${record.cost:.2f}")
        print(f"     Time: {record.timestamp.strftime('%H:%M:%S')}")
    print()
    
    # 4. Budget Checking
    print("4. Budget Checking")
    print("-" * 80)
    remaining = cost_mgr.get_remaining_budget()
    print(f"✓ Budget status:")
    print(f"  - Total cost: ${cost_mgr.total_cost:.2f}")
    print(f"  - Budget: ${cost_mgr.max_budget:.2f}")
    print(f"  - Remaining: ${remaining:.2f}")
    print(f"  - Percentage used: {(cost_mgr.total_cost / cost_mgr.max_budget * 100):.1f}%")
    print()
    
    # 5. Budget Enforcement
    print("5. Budget Enforcement")
    print("-" * 80)
    # Try to exceed budget
    try:
        # Add a large cost that exceeds budget
        cost_mgr.add_cost(15.0, role="Engineer", action="WriteCode")
        print("✗ Budget not enforced (unexpected)")
    except NoMoneyException as e:
        print(f"✓ Budget enforced correctly!")
        print(f"  - Exception: {e}")
        print(f"  - Total cost: ${e.total_cost:.2f}")
    print()
    
    # 6. Cost Summary
    print("6. Cost Summary")
    print("-" * 80)
    summary = cost_mgr.get_summary()
    print(f"✓ Summary:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  - {key}: ${value:.2f}")
        else:
            print(f"  - {key}: {value}")
    print()
    
    # 7. Resetting Costs
    print("7. Resetting Costs")
    print("-" * 80)
    cost_mgr.reset()
    print(f"✓ Cost manager reset:")
    print(f"  - Total cost: ${cost_mgr.total_cost:.2f}")
    print(f"  - Transactions: {len(cost_mgr.cost_history)}")
    print()
    
    print("=" * 80)
    print("Lesson 29 Complete!")
    print("=" * 80)
    print()
    print("Key Takeaways:")
    print("- CostManager tracks all API costs")
    print("- Budget limits prevent over-spending")
    print("- Cost history records all transactions")
    print("- Budget enforcement raises NoMoneyException")
    print("- Costs can be reset for new projects")


if __name__ == "__main__":
    asyncio.run(main())

