# Initializing the DocumentStore

from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack import Document

pgvector_store = PgvectorDocumentStore(
    embedding_dimension=384,
    vector_function="cosine_similarity",
    recreate_table=True,
    search_strategy="hnsw",
)