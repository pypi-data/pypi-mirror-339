import uuid
from datetime import datetime

import structlog

from curriculum_curator.content.transformer import ContentTransformer
from curriculum_curator.llm.manager import LLMManager
from curriculum_curator.persistence.manager import PersistenceManager
from curriculum_curator.prompt.registry import PromptRegistry
from curriculum_curator.validation.manager import ValidationManager
from curriculum_curator.workflow.engine import Workflow
from curriculum_curator.workflow.workflows import get_workflow_config

logger = structlog.get_logger()


class CurriculumCurator:
    """Main class that coordinates all components of the Curriculum Curator system."""

    def __init__(self, config, prompts_base_path=None):
        """Initialize the CurriculumCurator with configuration.

        Args:
            config: The configuration (either dict or AppConfig)
            prompts_base_path (str, optional): Override the base path for prompts
        """
        from curriculum_curator.config.models import AppConfig

        # Convert dict to AppConfig if needed
        if not isinstance(config, AppConfig):
            self.config = AppConfig.model_validate(config)
        else:
            self.config = config

        # Initialize components
        prompts_base_path = prompts_base_path or self.config.prompts.base_path
        self.prompt_registry = PromptRegistry(prompts_base_path)

        self.llm_manager = LLMManager(self.config)
        self.content_transformer = ContentTransformer()
        self.validation_manager = ValidationManager(self.config)
        self.persistence_manager = PersistenceManager(self.config)

        logger.info("curriculum_curator_initialized", prompts_base_path=prompts_base_path)

    def list_prompts(self, tag=None):
        """List available prompts, optionally filtered by tag.

        Args:
            tag (str, optional): Filter prompts by this tag

        Returns:
            list: List of prompt paths
        """
        return self.prompt_registry.list_prompts(tag)

    async def run_workflow(self, workflow_name, variables=None, session_id=None):
        """Run a workflow defined in the configuration or from predefined workflows.

        Args:
            workflow_name (str): Name of the workflow to run
            variables (dict, optional): Variables to pass to the workflow
            session_id (str, optional): Session ID for resuming a workflow

        Returns:
            dict: Results of the workflow execution
        """
        # First, try to get workflow from config
        workflow_config = None
        if hasattr(self.config, "workflows") and workflow_name in self.config.workflows:
            workflow_config = self.config.workflows[workflow_name]

        # If not found in config, try predefined workflows
        if not workflow_config:
            workflow_config = get_workflow_config(workflow_name)

        # If still not found, raise error
        if not workflow_config:
            raise ValueError(f"Workflow not found: {workflow_name}")

        # Create workflow instance
        workflow = Workflow(
            workflow_config,
            self.prompt_registry,
            self.llm_manager,
            self.content_transformer,
            self.validation_manager,
            self.persistence_manager,
        )

        # Set up initial context with provided variables
        context = variables or {}

        # Set workflow name and generate ID if not provided
        if not session_id:
            session_id = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"

        # Execute the workflow
        logger.info("workflow_starting", workflow_name=workflow_name, session_id=session_id)

        result = await workflow.execute(workflow_name, context, session_id)

        logger.info("workflow_completed", workflow_name=workflow_name, session_id=session_id)

        return result

    async def resume_workflow(self, session_id, from_step=None):
        """Resume a previously interrupted workflow.

        Args:
            session_id (str): The ID of the session to resume
            from_step (str, optional): The name of the step to resume from

        Returns:
            dict: Results of the resumed workflow execution
        """
        # Load session state
        session_data = self.persistence_manager.load_session(session_id)
        if not session_data:
            raise ValueError(f"Session not found: {session_id}")

        # Extract workflow name and context
        workflow_name = session_data.get("context", {}).get("workflow_name")
        if not workflow_name:
            raise ValueError("Invalid session data: missing workflow_name in context")

        # First, try to get workflow from config
        workflow_config = None
        if hasattr(self.config, "workflows") and workflow_name in self.config.workflows:
            workflow_config = self.config.workflows[workflow_name]

        # If not found in config, try predefined workflows
        if not workflow_config:
            workflow_config = get_workflow_config(workflow_name)

        # If still not found, raise error
        if not workflow_config:
            raise ValueError(f"Workflow not found: {workflow_name}")

        # Create workflow instance
        workflow = Workflow(
            workflow_config,
            self.prompt_registry,
            self.llm_manager,
            self.content_transformer,
            self.validation_manager,
            self.persistence_manager,
        )

        # Resume the workflow
        logger.info(
            "workflow_resuming",
            workflow_name=workflow_name,
            session_id=session_id,
            from_step=from_step,
        )

        result = await workflow.resume(session_id, from_step)

        logger.info(
            "workflow_resumed_completed", workflow_name=workflow_name, session_id=session_id
        )

        return result
