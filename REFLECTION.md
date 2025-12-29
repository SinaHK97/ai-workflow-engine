## Trade-offs Made

# 

## 1. Database & Storage Considerations

Although this project focuses on abstractions rather than implementation, a real system would require multiple storage layers, each optimized for a specific workload.

### Relational Database (Metadata & Configuration)

A relational database (e.g. PostgreSQL) would be used to store:

* Organizations and sub-organizations
* Knowledge collection metadata
* Workflow definitions and versions
* Workflow executions and execution summaries

This provides:

* Strong consistency for configuration data
* Clear ownership boundaries via `org_id` and `sub_org_id`
* Easy querying for observability and auditing

Workflow definitions are stored as immutable JSON blobs per version, ensuring reproducibility.

---

### Vector Store (Embeddings & Retrieval)

Document chunks and their embeddings would be stored in a vector database (e.g. FAISS, Pinecone, Weaviate).

Key considerations:

* Chunk-level embeddings enable fine-grained retrieval
* Collection-level filtering ensures tenant isolation
* Embedding model version is stored to avoid incompatibilities

The vector store is treated as an **external dependency**, keeping the core engine storage-agnostic.

---

### Object Storage (Raw Documents)

Original documents (PDFs, text files) would be stored in object storage (e.g. S3-compatible).

Benefits:

* Cheap, scalable storage
* Decouples raw content from embeddings
* Allows re-chunking or re-embedding if models change

---

## 2. Error Handling Strategy

Error handling is designed around **isolation, visibility, and graceful failure**.

### Design-Time Errors (Validation)

Errors caught before execution:

* Missing or duplicate step IDs
* Invalid step references
* Missing required parameters per step type
* Multiple or missing entry steps

Invalid workflows are rejected before activation.

---

### Runtime Errors

Errors during execution (e.g. LLM timeout, RAG failure) are:

* Captured at the **step level**
* Logged in structured execution logs
* Propagated to the workflow execution status

Depending on the step type, failures may:

* Fail the workflow immediately
* Route to a fallback step
* Return a partial but valid response

This allows flexibility without hiding failures.

---

## 3. Multi-Tenancy & Isolation

Multi-tenancy is a **first-class design concern**.

### Tenant Boundaries

Every entity explicitly includes:

* `org_id`
* `sub_org_id`

This ensures:

* No implicit cross-tenant access
* Easy enforcement of isolation at query time
* Compatibility with row-level security if needed

---

### Execution Isolation

Each workflow execution:

* Has its own execution context
* Cannot read or mutate state from other executions
* Operates only on knowledge collections owned by the same tenant

This prevents data leakage and simplifies reasoning about execution behavior.

---

## 4. Scalability & Performance Considerations

While not implemented, the design supports scaling:

* Workflow execution can be made asynchronous
* Step handlers can be stateless and horizontally scalable
* RAG and LLM calls can be rate-limited or retried independently
* Execution logs can be sampled or summarized to reduce storage load

The linear-first execution model keeps control flow simple and predictable under load.

---

## 5. Observability & Debugging

Observability is treated as a core feature, not an afterthought.

Each execution records:

* Workflow version used
* Execution duration
* Step-by-step status and timing
* Error messages where applicable

This enables:

* Debugging failed workflows
* Auditing model behavior
* Performance analysis over time

---

## 6. Security & Access Control (Out of Scope but Considered)

Authentication and authorization are intentionally out of scope, but the design supports:

* Per-tenant access control
* Workflow ownership enforcement
* Knowledge access restrictions

All APIs would require tenant context to be explicitly provided.

---

## 7. Trade-offs Made

* Chose linear execution with conditional branching over full DAGs to reduce complexity
* Prioritized immutability and versioning over mutable workflows
* Kept metadata schema-light to allow flexibility
* Deferred human-in-the-loop and long-running workflows

These decisions favor clarity and maintainability over maximum expressiveness.

---

## 8. What I Would Improve With More Time

* Full DAG support with cycle detection
* Asynchronous execution and retries
* Human approval steps
* Schema validation per step type
* Visual workflow editor integration
* Fine-grained cost and token usage tracking

---

## 9. Testing Strategy

A comprehensive testing approach would include:

* **Unit tests**
  * Step handlers
  * Placeholder resolution
* **Integration tests**
  * End-to-end workflow execution with mocks
* **Validation tests**
  * Invalid workflow definitions
* **Load tests**
  * Concurrent executions
  * Large knowledge collections

---

## 10. Use of AI Tools

AI tools were used for:

* Brainstorming system structure
* Refining abstractions
* Improving clarity and documentation quality

All outputs were reviewed and validated to ensure correctness and consistency with the design goals.

* Chose **linear execution with conditional jumps** instead of a full DAG to reduce complexity.
* Used **schema-light metadata** for knowledge objects to allow flexibility.
* Prioritized **immutability and versioning** over in-place updates.

---

## Improvements With More Time

* Add async execution and retries.
* Introduce workflow visual validation.
* Add human-in-the-loop approval steps.
* Implement loop detection and execution limits.

---

## Testing Strategy

* **Unit tests**
  * Step handlers
  * Template resolution
* **Integration tests**
  * Full workflow execution with mock services
* **Validation tests**
  * Invalid workflows
  * Missing references
* **Load tests**
  * Concurrent executions
  * Large knowledge collections

---


## Integration with Agent-to-UI Frameworks (e.g. Google A2UI)

While the scope of this project is focused on backend abstractions, the design intentionally supports integration with agent-to-UI frameworks such as **Google’s A2UI**.

A2UI enables agents to return **structured UI descriptions** (forms, tables, actions) rather than raw text, allowing the frontend to dynamically render interfaces based on agent output. This fits naturally into the workflow-based architecture by treating UI schemas as **structured step outputs**, not as part of the execution engine itself.

In this design, A2UI-compatible outputs could be produced by an `LLM` step and passed through a dedicated terminal step (e.g. `UI_RESPONSE`). The workflow engine remains UI-agnostic and simply propagates structured data, while the frontend is responsible for rendering and user interaction.

This separation preserves:

* Clear boundaries between backend orchestration and presentation logic
* Extensibility for future UI-driven agent interactions
* Compatibility with multiple UI frameworks, not just A2UI

The integration is optional and does not affect the core execution model, reinforcing the system’s flexibility without introducing additional coupling or complexity.

## Use of AI Tools

AI tools were used to:

* Brainstorm step types
* Validate architectural patterns
* Improve clarity of documentation

All outputs were reviewed, simplified, and aligned with the system’s goals.
