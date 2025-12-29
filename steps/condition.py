class ConditionStepHandler(BaseStepHandler):
    step_type = "LLM"

    def execute(self, step, context):
        ## Find the next step and set it
        ## step.next_step = ...
        return {}
