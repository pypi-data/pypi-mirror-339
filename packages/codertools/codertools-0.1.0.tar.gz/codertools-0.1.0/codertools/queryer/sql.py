from pinecone import Pinecone
from pinecone import ServerlessSpec
import os


def get_pinecone_index():
    index="api-documents-index"
    space="pydantic"
    pc = Pinecone(api_key=os.environ.get("pinecone_key"))
    return pc.Index(index)
