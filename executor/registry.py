from steps.base import BaseStepHandler


class StepRegistry:
    def __init__(self):
        self._handlers = {}

    def register(self, handler: BaseStepHandler):
        self._handlers[handler.step_type] = handler

    def get(self, step_type: str) -> BaseStepHandler:
        if step_type not in self._handlers:
            raise ValueError(f"Unsupported step type: {step_type}")
        return self._handlers[step_type]
