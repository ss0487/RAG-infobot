from haystack.components.preprocessors import DocumentSplitter

sentence_splitter = DocumentSplitter(
    split_by="sentence",
    split_length=5,
)