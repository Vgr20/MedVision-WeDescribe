from llama_index.core import ServiceContext

def service_context(llm_model,embedding_model):  
    service_context = ServiceContext.from_defaults(
        chunk_size = 1024,
        llm = llm_model,
        embed_model = embedding_model
    )
    return service_context
