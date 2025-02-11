# Initialize a Document Embedder

from haystack.components.embedders import SentenceTransformersDocumentEmbedder

sentence_trf_embedder = SentenceTransformersDocumentEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2",
)
# sentence_trf_embedder.warm_up()