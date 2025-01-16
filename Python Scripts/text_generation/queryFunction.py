from serviceContext import service_context
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

def vector_store_index(document_path,llm_model,embedding_model):
    documents = SimpleDirectoryReader(document_path).load_data()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context(llm_model,embedding_model))
    return index

def query_engine_object(llm_model,embedding_model):
    data_path = '/content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/data_stream'
    query_engine = vector_store_index(data_path,llm_model,embedding_model).as_query_engine()
    return query_engine

################################ function call##############################