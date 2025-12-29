class WorkflowExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, workflow, input_payload):
        context = {
            "input": input_payload,
            "steps": {}
        }

        current_step_id = workflow.entry_step

        while current_step_id:
            step = workflow.get_step(current_step_id)
            handler = self.registry.get(step.step_type)

            output = handler.execute(step, context)
            ## Create execution step log
            context["steps"][step.step_id] = output
            current_step_id = step.next_step

        ## Create WorkflowExecutionLog

        return context
