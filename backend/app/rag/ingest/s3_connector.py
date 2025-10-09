from typing import Any, Dict, List

import boto3

from .base_connector import BaseConnector


class S3Connector(BaseConnector):
    """
    Connector for fetching documents from an AWS S3 bucket.
    """

    def __init__(self, region_name: str = "us-east-1"):
        # In a real app, credentials would be configured securely
        self.s3_client = boto3.client("s3", region_name=region_name)

    async def fetch(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Fetches a file from an S3 bucket.

        Args:
        ----
            source: A dictionary containing 'bucket' and 'key'.

        Returns:
        -------
            A list containing a single dictionary with the file's
            content and metadata.

        """
        bucket = source["bucket"]
        key = source["key"]

        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read()

        return [
            {
                "content": content,
                "metadata": {
                    "source": "s3",
                    "bucket": bucket,
                    "key": key,
                    "size_bytes": len(content),
                },
            }
        ]
