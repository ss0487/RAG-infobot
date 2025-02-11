# Fetching and Indexing Documents

from haystack import Pipeline, Document
from doc_pipeline_components.converter import pdf_to_docs
from doc_pipeline_components.cleaner import doc_cleaner
from doc_pipeline_components.null_replacer import denuller
from doc_pipeline_components.splitter import sentence_splitter
from doc_pipeline_components.embedder import sentence_trf_embedder
from doc_pipeline_components.writer import pg_vector_writer

indexing_pipeline = Pipeline()

indexing_pipeline.add_component("converter", pdf_to_docs)
indexing_pipeline.add_component("cleaner", doc_cleaner)
indexing_pipeline.add_component("denuller", denuller)
indexing_pipeline.add_component("splitter", sentence_splitter)
indexing_pipeline.add_component("embedder", sentence_trf_embedder)
indexing_pipeline.add_component("writer", pg_vector_writer)
indexing_pipeline.connect("converter", "cleaner")
indexing_pipeline.connect("cleaner", "denuller")
indexing_pipeline.connect("denuller", "splitter")
indexing_pipeline.connect("splitter", "embedder")
indexing_pipeline.connect("embedder", "writer")

print("\nCreated indexing pipeline.\n")