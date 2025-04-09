'''
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

filters = MetadataFilters(
    filters=[
        MetadataFilter(
            key="theme", operator=FilterOperator.EQ, value="Fiction"
        ),
    ]
)
'''

from reader import read_github_repo,read_github_issue
from sql import get_pinecone_index
from adapter import PineconeAdapter

def build():
    
    # get documents
    docs_document = read_github_repo(owner="pydantic",repo="pydantic")
    issue_document = read_github_issue(owner="pydantic",repo="pydantic")

    # splitter # TODO
    nodes = docs_document

    # get_store
    pc_index = get_pinecone_index
    storage_context = PineconeAdapter(index,space).get_storage_context()

    # build_index
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    
    retriever = index.as_retriever(filters=filters)
    retriever.retrieve("What is inception about?")
