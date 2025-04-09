"""
模型适配器
"""

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore



class StorageAdapter:
    def __init__(self):
        self.index = None
        
    def get_storage_context(self)->any:
        raise NotImplementedError("This method should be implemented by subclasses")




class PineconeAdapter(StorageAdapter):
    def __init__(self,index,space:str):
        super().__init__()
        self.index = index
        self.space = space
        
    def get_storage_context(self):
        vector_store = PineconeVectorStore(pinecone_index=self.index,namespace = self.space)
        return StorageContext.from_defaults(vector_store=vector_store)


