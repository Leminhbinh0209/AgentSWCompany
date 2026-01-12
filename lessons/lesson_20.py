"""
Lesson 20: Advanced Actions
============================

This lesson demonstrates advanced action patterns and action graphs.

Run this lesson:
    python lesson_20.py
"""
import sys
import os
import asyncio

# Add parent directory to path to import framework
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tutorial_example'))
from framework.actions.advanced.action_graph import ActionGraph
from framework.action import Action
from framework.schema import Message, ActionOutput
from framework.llm import get_llm
from typing import List, Optional


class SimpleAction(Action):
    def __init__(self, name: str, output: str, llm=None):
        super().__init__(name=name, llm=llm)
        self.output = output
    
    async def run(self, messages: Optional[List[Message]] = None, **kwargs) -> ActionOutput:
        return ActionOutput(content=self.output, instruct_content={"action": self.name})


async def main():
    print("=" * 60)
    print("Lesson 20: Advanced Actions")
    print("=" * 60)
    print()
    
    # Create action graph
    print("1. Creating Action Graph")
    print("-" * 60)
    graph = ActionGraph()
    
    action1 = SimpleAction("Action1", "Result 1", llm=get_llm())
    action2 = SimpleAction("Action2", "Result 2", llm=get_llm())
    
    # Add actions to graph (node2 depends on node1)
    node1_id = graph.add_action(action1, node_id="node1")
    node2_id = graph.add_action(action2, node_id="node2", dependencies=["node1"])
    
    print(f"Graph created with {len(graph.nodes)} nodes")
    print()
    
    # Execute graph
    print("2. Executing Action Graph")
    print("-" * 60)
    results = await graph.execute()
    print(f"Status: {results['status']}")
    print(f"Completed: {len(results['completed'])} actions")
    print(f"Results: {results['results']}")
    print()
    
    print("=" * 60)
    print("Lesson 20 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

