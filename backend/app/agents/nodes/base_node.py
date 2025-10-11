from abc import ABC, abstractmethod
from typing import Dict, Any

from app.agents.state import AgentState

class BaseNode(ABC):
    """
    Abstract base class for all agent nodes.
    Each node is an asynchronous callable that modifies the agent state.
    """
    @abstractmethod
    async def __call__(self, state: AgentState) -> AgentState:
        """
        Processes the current agent state and returns the updated state.

        Args:
            state: The current state of the agent graph.

        Returns:
            The modified agent state.
        """
        pass