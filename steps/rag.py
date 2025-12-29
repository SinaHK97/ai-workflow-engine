from steps.base import BaseStepHandler


class RAGStepHandler(BaseStepHandler):
    step_type = "RAG"

    def execute(self, step, context):
        query = resolve_template(step.params["query"], context)
        chunks = vector_search(
            collection_id=step.params["collection_id"],
            query=query,
            top_k=step.params["top_k"]
        )
        return {
            "chunks": chunks
        }
