from haystack.components.writers import DocumentWriter
from document_store import pgvector_store

pg_vector_writer = DocumentWriter(document_store=pgvector_store)