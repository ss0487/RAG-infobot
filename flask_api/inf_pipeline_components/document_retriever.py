# Initialize the Retriever

from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever

from document_store import pgvector_store

retriever = PgvectorEmbeddingRetriever(document_store=pgvector_store)