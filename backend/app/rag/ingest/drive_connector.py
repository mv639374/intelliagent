from typing import Any, Dict, List

from .base_connector import BaseConnector


class DriveConnector(BaseConnector):
    """
    Stub connector for Google Drive.
    TODO: This will be fully implemented in Phase 2 using the MCP.
    """

    async def fetch(self, source: Any) -> List[Dict[str, Any]]:
        print("Google Drive Connector is not yet implemented.")
        # This will eventually use OAuth tokens from the MCP to fetch files
        return []
