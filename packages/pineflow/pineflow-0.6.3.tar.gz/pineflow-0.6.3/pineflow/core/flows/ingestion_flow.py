
from typing import List, Optional

from pineflow.core.document.schema import Document, TransformerComponent
from pineflow.core.readers.base import BaseReader


class IngestionFlow():
    """An ingestion flow.

    Args:
        transformers: Transformers to apply to the data.
        readers (BaseReader, optional): Reader to use to ingest data.

    **Example**

    .. code-block:: python

        from pineflow.core.flows import IngestionFlow
        from pineflow.text_chunkers import TokenTextChunker
        from pineflow.embeddings import HuggingFaceEmbedding

        
        ingestion_flow = IngestionFlow(transformers= [
            TokenTextChunker(), 
            HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-small"),
            ]
        )
    """

    def __init__(self, 
                 transformers: TransformerComponent,
                 readers: List[BaseReader]=None):
        
        self.transformers = transformers
        self.readers = readers
    
    def _read_documents(self, documents: Optional[List[Document]]):
        input_documents = []
        
        if documents is not None:
            input_documents.extend(documents)
            
        if self.readers is not None:
            for reader in self.readers:
                input_documents.extend(reader.load_data())
        
        return input_documents    
        
    def _run_transformers(self, documents: List[Document], transformers: TransformerComponent):
        for transform in transformers:
            documents = transform(documents)
        
        return documents    
    
    def run(self, documents: List[Document]=None):
        """An ingestion flow.

        Args:
            documents: Set of documents to be transformed.

        **Example**

        .. code-block:: python

            ingestion_flow.run(documents: List[Document])
        """
        input_documents = self._read_documents(documents)
        
        documents = self._run_transformers(input_documents, self.transformers)
        
        return documents or []    
        
