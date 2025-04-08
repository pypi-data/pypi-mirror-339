from typing import Optional

from vector_bridge import VectorBridgeClient
from vector_bridge.schema.workflows import PaginatedWorkflows


class WorkflowsAdmin:
    """Admin client for workflows management endpoints."""

    def __init__(self, client: VectorBridgeClient):
        self.client = client

    def list_workflows(
        self,
        integration_name: str = None,
        limit: int = 25,
        last_evaluated_key: Optional[str] = None,
        sort_by: str = "created_at",
    ) -> PaginatedWorkflows:
        """
        List Workflows for an Integration, sorted by created_at or updated_at.

        Args:
            integration_name: The name of the Integration
            limit: The number of Workflows to retrieve
            last_evaluated_key: Pagination key for the next set of results
            sort_by: The sort field (created_at or updated_at)

        Returns:
            PaginatedWorkflows with workflows and pagination info
        """
        if integration_name is None:
            integration_name = self.client.integration_name

        url = f"{self.client.base_url}/v1/admin/workflows/list"
        params = {
            "integration_name": integration_name,
            "limit": limit,
            "sort_by": sort_by,
        }
        if last_evaluated_key:
            params["last_evaluated_key"] = last_evaluated_key

        headers = self.client._get_auth_headers()
        response = self.client.session.get(url, headers=headers, params=params)
        result = self.client._handle_response(response)
        return PaginatedWorkflows.model_validate(result)

    def delete_workflow(self, workflow_id: str, integration_name: str = None) -> None:
        """
        Delete Workflow from the integration.

        Args:
            workflow_id: The workflow ID
            integration_name: The name of the Integration
        """
        if integration_name is None:
            integration_name = self.client.integration_name

        url = f"{self.client.base_url}/v1/admin/workflows/{workflow_id}/delete"
        params = {"integration_name": integration_name}
        headers = self.client._get_auth_headers()
        response = self.client.session.delete(url, headers=headers, params=params)
        self.client._handle_response(response)
