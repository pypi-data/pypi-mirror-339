import hashlib
import io
import json
import sys
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from functools import wraps
from typing import Any

from vector_bridge import VectorBridgeClient
from vector_bridge.schema.workflows import (WorkflowCache, WorkflowCreate,
                                            WorkflowData, WorkflowStatus,
                                            WorkflowUpdate)


class WorkflowClient:
    """Client for workflow endpoints that require an API key."""

    def __init__(self, client: VectorBridgeClient):
        self.client = client

    def add_workflow(self, workflow_create: WorkflowCreate, integration_name: str = None) -> WorkflowData:
        """
        Add new Workflow to the integration.

        Args:
            workflow_create: The Workflow data to create
            integration_name: The name of the Integration

        Returns:
            Created workflow object
        """
        if integration_name is None:
            integration_name = self.client.integration_name

        url = f"{self.client.base_url}/v1/workflow/create"
        params = {"integration_name": integration_name}
        headers = self.client._get_api_key_headers(self.client.api_key)
        response = self.client.session.post(url, headers=headers, params=params, json=workflow_create.model_dump())
        result = self.client._handle_response(response)
        return WorkflowData.model_validate(result)

    def get_workflow(self, workflow_id: str, integration_name: str = None) -> WorkflowData:
        """
        Retrieve Workflow by ID.

        Args:
            workflow_id: The ID of the Workflow
            integration_name: The name of the Integration

        Returns:
            Workflow object
        """
        if integration_name is None:
            integration_name = self.client.integration_name

        url = f"{self.client.base_url}/v1/workflow/{workflow_id}"
        params = {"integration_name": integration_name}
        headers = self.client._get_api_key_headers(self.client.api_key)
        response = self.client.session.get(url, headers=headers, params=params)
        result = self.client._handle_response(response)
        return WorkflowData.model_validate(result)

    def update_workflow(
        self,
        workflow_id: str,
        workflow_update: WorkflowUpdate,
        integration_name: str = None,
    ) -> WorkflowData:
        """
        Update an existing Workflow.

        Args:
            workflow_id: The ID of the Workflow
            workflow_update: The Workflow updates
            integration_name: The name of the Integration

        Returns:
            Updated workflow object
        """
        if integration_name is None:
            integration_name = self.client.integration_name

        url = f"{self.client.base_url}/v1/workflow/{workflow_id}/update"
        params = {"integration_name": integration_name}
        headers = self.client._get_api_key_headers(self.client.api_key)
        response = self.client.session.put(url, headers=headers, params=params, json=workflow_update.model_dump())
        result = self.client._handle_response(response)
        return WorkflowData.model_validate(result)


# Output capturing context manager
class CaptureOutput:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self._stdout_backup = None
        self._stderr_backup = None

    def __enter__(self):
        # Save original stdout/stderr and redirect to our buffers
        self._stdout_backup = sys.stdout
        self._stderr_backup = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original stdout/stderr
        sys.stdout = self._stdout_backup
        sys.stderr = self._stderr_backup

    def get_output(self) -> str:
        """Get captured stdout and stderr content"""
        return self.stdout.getvalue() + self.stderr.getvalue()


def generate_dynamodb_key(workflow_id, method, args, kwargs):
    method_name = method.__name__

    # Convert args to a string-safe format
    args_str = "_".join(map(str, args)) if args else "no_args"

    # Convert kwargs to key-value pairs, sorted for consistency
    kwargs_str = "_".join(f"{k}-{v}" for k, v in sorted(kwargs.items())) if kwargs else "no_kwargs"

    # Ensure no special characters
    key = f"workflow_{workflow_id}_{method_name}_{args_str}_{kwargs_str}"

    # Truncate if necessary (DynamoDB keys should not be too long)
    return method_name + "__" + hashlib.sha256(key.encode()).hexdigest()  # Use SHA-256 for long keys


# Method-level caching decorator
def cache_result(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate a deterministic cache key
        cache_key = generate_dynamodb_key(self.workflow_id, method, args, kwargs)

        # Try to get from cache
        cached_data = self.get_cache(cache_key)
        if cached_data is not None and isinstance(cached_data, WorkflowCache):
            if not cached_data.traceback:
                print(f"Cache hit for {cache_key}")
                return json.loads(cached_data.result)

        print(f"Cache miss for {cache_key}")

        # Capture all output
        with CaptureOutput() as output:
            start_time = datetime.now(timezone.utc)
            result = None
            traceback_info = None

            try:
                # Execute the method
                result = method(self, *args, **kwargs)
                return result
            except Exception:
                # Capture error information
                traceback_info = traceback.format_exc()
                raise
            finally:
                # Create workflow cache for this execution
                end_time = datetime.now(timezone.utc)

                workflow_cache = WorkflowCache(
                    method_name=method.__name__,
                    args=list(args),
                    kwargs=kwargs,
                    started_at=start_time.isoformat(),
                    processed_at=end_time.isoformat(),
                    processing_time=(end_time - start_time).total_seconds(),
                    logs=output.get_output(),
                    traceback=traceback_info,
                    result=json.dumps(result),
                )

                # Update cache with the results
                self.set_cache(cache_key, workflow_cache)

    return wrapper


# Main workflow execution decorator
def workflow_runner(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate a deterministic cache key
        cache_key = generate_dynamodb_key(self.workflow_id, method, args, kwargs)

        # Try to get from cache
        cached_data = self.get_cache(cache_key)
        if cached_data is not None and isinstance(cached_data, WorkflowCache):
            if self.workflow_data.status == WorkflowStatus.COMPLETED:
                print(f"Workflow cache hit for {cache_key}")
                return json.loads(cached_data.result)

        print(f"Workflow cache miss for {cache_key}")

        # Update status to in progress
        self.update_status(WorkflowStatus.IN_PROGRESS)

        # Capture all output
        with CaptureOutput() as output:
            start_time = datetime.now(timezone.utc)
            result = None
            traceback_info = None

            try:
                # Execute the workflow method
                result = method(self, *args, **kwargs)

                # Update status to completed on success
                self.update_status(WorkflowStatus.COMPLETED)
                return result

            except Exception:
                # Capture error information
                traceback_info = traceback.format_exc()

                # Update status to failed
                self.update_status(WorkflowStatus.FAILED)
                raise

            finally:
                # Always record execution details
                end_time = datetime.now(timezone.utc)

                # Create workflow cache entry
                workflow_cache = WorkflowCache(
                    method_name=method.__name__,
                    args=list(args),
                    kwargs=kwargs,
                    started_at=start_time.isoformat(),
                    processed_at=end_time.isoformat(),
                    processing_time=(end_time - start_time).total_seconds(),
                    logs=output.get_output(),
                    traceback=traceback_info,
                    result=json.dumps(result),
                )

                # Cache the execution results
                self.set_cache(cache_key, workflow_cache)

    return wrapper


class Workflow(ABC):
    """
    Abstract base class for building workflow processes with automatic caching and status tracking.

    This class serves as a foundation for creating workflow implementations that need:
    - Status tracking (pending, in-progress, completed, failed)
    - Automatic caching of intermediate results
    - Output and error capture

    Usage:
        1. Create a custom class inheriting from Workflow
        2. Implement a main method decorated with @workflow_runner
        3. Implement individual processing steps decorated with @cache_result

    Example:
        class MyWorkflow(Workflow):
            @workflow_runner
            def run(self, input_data):
                # Main workflow execution
                data = self.fetch_data(input_data)
                results = self.process_data(data)
                return self.generate_report(results)

            @cache_result
            def fetch_data(self, input_id):
                # This result will be cached
                # ...fetch logic here...
                return data

            @cache_result
            def process_data(self, data):
                # This result will be cached
                # ...processing logic here...
                return processed_data

            @cache_result
            def generate_report(self, processed_data):
                # This result will be cached
                # ...report generation logic here...
                return report

        # Usage:
        workflow = MyWorkflow(client, workflow_id)
        result = workflow.run("input123")
    """

    def __init__(self, client: VectorBridgeClient, workflow_create: WorkflowCreate):
        self.client = client
        self.workflow_id = workflow_create.workflow_id
        self.workflow_data: WorkflowData = self.client.workflows.add_workflow(workflow_create)

    @abstractmethod
    def run(self):
        pass

    def refresh(self):
        """Refresh workflow data from the server"""
        self.workflow_data = self.client.workflows.get_workflow(self.workflow_id)

    def update_status(self, status: WorkflowStatus):
        """Update the workflow status"""
        self.workflow_data = self.client.workflows.update_workflow(
            workflow_id=self.workflow_id, workflow_update=WorkflowUpdate(status=status)
        )

    @property
    def status(self) -> WorkflowStatus:
        """Get the current workflow status"""
        return self.workflow_data.status

    def get_cache(self, key: str) -> Any:
        """Get value from workflow cache"""
        if not self.workflow_data.cache:
            return None
        return self.workflow_data.cache.get(key)

    def set_cache(self, key: str, value: WorkflowCache):
        """Set value in workflow cache"""
        # Update workflow with new cache using WorkflowUpdate structure
        self.workflow_data = self.client.workflows.update_workflow(
            workflow_id=self.workflow_id,
            workflow_update=WorkflowUpdate(cache={key: value}),
        )
