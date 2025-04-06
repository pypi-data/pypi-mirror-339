from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ConfigDict

from ..state import RunContext


class BaseStep(BaseModel, ABC):
    """Abstract base class for defining processing steps in a workflow.

    BaseStep combines Pydantic's data validation with abstract methods to create a
    standardized interface for workflow steps. Each step must define its parameter
    and return value schemas, as well as the actual processing logic.
    """
    # Allow storing extra fields in the model.
    model_config = ConfigDict(extra="allow")

    id: str 
    """Unique identifier for the step instance."""
    path: str 
    """Any step will be a part of a flow. With potentially multiple nested sub-flows.
    We will use the path to uniquely identify the step's position in the overall flow.
    """
    metadata: dict[str, Any] = {}
    """Optional metadata associated with the step."""


    @abstractmethod
    def params_model(self) -> BaseModel:
        """Returns the Pydantic model defining the expected parameters for this step."""
        pass


    @abstractmethod
    def params_model_schema(self) -> dict[str, Any]:
        """Returns the JSON schema for the step's parameter model."""
        pass
    

    @abstractmethod
    def return_model(self) -> Any:
        """Returns the expected return type for this step."""
        pass


    @abstractmethod
    def return_model_schema(self) -> dict[str, Any]:
        """Returns the JSON schema for the step's return value model."""
        pass


    # TODO Better method definition. Then we can use "See base class" in the child classes.
    @abstractmethod
    def run(
        self, 
        context: RunContext | None = None, # noqa: ARG002
        **kwargs: Any,
    ) -> Any:
        """Executes the step's processing logic."""
        pass
