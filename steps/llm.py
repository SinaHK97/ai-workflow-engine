class LLMStepHandler(BaseStepHandler):
    step_type = "LLM"

    def execute(self, step, context):
        prompt = resolve_template(step.params["prompt_template"], context)
        response = call_llm(
            model=step.params["model"],
            prompt=prompt
        )
        return {
            "text": response.text,
            "confidence": response.confidence
        }
