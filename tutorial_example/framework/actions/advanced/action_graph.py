"""Action Graph for managing action dependencies and execution order"""
from typing import Dict, List, Optional, Set, Any
from framework.action import Action
from framework.schema import Message, ActionOutput


class ActionNode:
    """Node in action graph representing an action with dependencies"""
    
    def __init__(self, action: Action, node_id: Optional[str] = None):
        """
        Initialize Action Node
        
        Args:
            action: Action instance
            node_id: Optional node ID (defaults to action name)
        """
        self.action = action
        self.node_id = node_id or action.name
        self.dependencies: List[str] = []  # IDs of dependent nodes
        self.dependents: List[str] = []  # IDs of nodes that depend on this
        self.completed = False
        self.failed = False
        self.result: Optional[ActionOutput] = None
        self.error: Optional[str] = None
    
    def add_dependency(self, node_id: str):
        """Add a dependency"""
        if node_id not in self.dependencies:
            self.dependencies.append(node_id)
    
    def can_execute(self, completed_nodes: Set[str]) -> bool:
        """
        Check if this node can be executed
        
        Args:
            completed_nodes: Set of completed node IDs
            
        Returns:
            True if all dependencies are completed
        """
        return all(dep_id in completed_nodes for dep_id in self.dependencies)
    
    def mark_completed(self, result: ActionOutput):
        """Mark node as completed"""
        self.completed = True
        self.result = result
    
    def mark_failed(self, error: str):
        """Mark node as failed"""
        self.failed = True
        self.error = error


class ActionGraph:
    """Graph of actions with dependencies for workflow management"""
    
    def __init__(self):
        """Initialize Action Graph"""
        self.nodes: Dict[str, ActionNode] = {}
        self.execution_order: List[List[str]] = []
    
    def add_action(self, action: Action, node_id: Optional[str] = None, 
                  dependencies: Optional[List[str]] = None) -> str:
        """
        Add an action to the graph
        
        Args:
            action: Action to add
            node_id: Optional node ID
            dependencies: List of node IDs this depends on
            
        Returns:
            Node ID
        """
        node = ActionNode(action, node_id)
        node_id = node.node_id
        
        if dependencies:
            node.dependencies = dependencies
            # Update dependents
            for dep_id in dependencies:
                if dep_id in self.nodes:
                    if node_id not in self.nodes[dep_id].dependents:
                        self.nodes[dep_id].dependents.append(node_id)
        
        self.nodes[node_id] = node
        return node_id
    
    def get_executable_actions(self) -> List[ActionNode]:
        """
        Get actions that can be executed now (all dependencies completed)
        
        Returns:
            List of executable action nodes
        """
        completed_ids = {
            node_id for node_id, node in self.nodes.items()
            if node.completed
        }
        
        executable = []
        for node in self.nodes.values():
            if not node.completed and not node.failed and node.can_execute(completed_ids):
                executable.append(node)
        
        return executable
    
    def get_execution_order(self) -> List[List[str]]:
        """
        Get execution order using topological sort
        
        Returns:
            List of node ID lists, each list can be executed in parallel
        """
        # Build dependency graph
        in_degree = {node_id: len(node.dependencies) for node_id, node in self.nodes.items()}
        graph = {node_id: [] for node_id in self.nodes.keys()}
        
        for node in self.nodes.values():
            for dep_id in node.dependencies:
                if dep_id in graph:
                    graph[dep_id].append(node.node_id)
        
        # Topological sort
        result = []
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        
        while queue:
            level = []
            next_queue = []
            
            for node_id in queue:
                level.append(node_id)
                for dependent_id in graph[node_id]:
                    in_degree[dependent_id] -= 1
                    if in_degree[dependent_id] == 0:
                        next_queue.append(dependent_id)
            
            if level:
                result.append(level)
            queue = next_queue
        
        self.execution_order = result
        return result
    
    async def execute(self, context: Optional[Dict[str, Any]] = None, 
                     messages: Optional[List[Message]] = None) -> Dict[str, Any]:
        """
        Execute the action graph
        
        Args:
            context: Optional context dictionary
            messages: Optional initial messages
            
        Returns:
            Dict with execution results
        """
        results = {
            "status": "success",
            "completed": [],
            "failed": [],
            "results": {}
        }
        
        # Set context for all actions
        if context:
            for node in self.nodes.values():
                node.action.set_context(context)
        
        # Get execution order
        execution_order = self.get_execution_order()
        
        # Execute in order
        for level in execution_order:
            # Execute all actions in this level (can be parallel)
            for node_id in level:
                node = self.nodes[node_id]
                
                try:
                    # Execute action
                    output = await node.action.run(messages=messages)
                    node.mark_completed(output)
                    results["completed"].append(node_id)
                    results["results"][node_id] = output.content
                    
                    # Add output to messages for next actions
                    if messages is None:
                        messages = []
                    message = output.to_message(
                        role="ActionGraph",
                        cause_by=node.action.name
                    )
                    messages.append(message)
                    
                except Exception as e:
                    node.mark_failed(str(e))
                    results["failed"].append(node_id)
                    results["status"] = "partial" if results["completed"] else "failed"
                    results["results"][node_id] = f"Error: {str(e)}"
        
        return results
    
    def get_node(self, node_id: str) -> Optional[ActionNode]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
    
    def reset(self):
        """Reset all nodes to initial state"""
        for node in self.nodes.values():
            node.completed = False
            node.failed = False
            node.result = None
            node.error = None
    
    def get_status(self) -> Dict[str, Any]:
        """Get graph execution status"""
        total = len(self.nodes)
        completed = sum(1 for n in self.nodes.values() if n.completed)
        failed = sum(1 for n in self.nodes.values() if n.failed)
        pending = total - completed - failed
        
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }

