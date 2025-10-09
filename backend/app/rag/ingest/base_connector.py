from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseConnector(ABC):
    """
    Abstract base class for data source connectors.
    """

    @abstractmethod
    async def fetch(self, source: Any) -> List[Dict[str, Any]]:
        """
        Fetch data from the source and return it as a list of documents.
        Each document is a dictionary with 'content' and 'metadata'.
        """
        pass
