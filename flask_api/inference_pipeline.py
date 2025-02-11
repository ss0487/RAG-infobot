### Building the RAG Pipeline
### Create new pipeline

from haystack import Pipeline
from inf_pipeline_components.query_processor import text_embedder
from inf_pipeline_components.document_retriever import retriever
from inf_pipeline_components.prompt_builder import context_prompt_builder
from inf_pipeline_components.generator import llama_generator


rag_inf_pipeline = Pipeline()

### Add components to your pipeline

rag_inf_pipeline.add_component("text_embedder", text_embedder)
rag_inf_pipeline.add_component("retriever", retriever)
rag_inf_pipeline.add_component("prompt_builder", context_prompt_builder)
rag_inf_pipeline.add_component("llm", llama_generator)

### Now, connect the components to each other
rag_inf_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
rag_inf_pipeline.connect("retriever", "prompt_builder.documents")
rag_inf_pipeline.connect("prompt_builder", "llm")

print("\nCreated inference pipeline.\n")
