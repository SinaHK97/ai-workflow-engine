from abc import ABC, abstractmethod
from executor.context import ExecutionContext


class BaseStepHandler(ABC):
    step_type: str

    @abstractmethod
    def execute(self, step, context) -> dict:
        pass
    

    @classmethod
    def resolve_template(template: str, context: dict) -> str:
        # Minimal example
        # Replace {{ steps.s01.text }} with actual value
        return rendered_string

