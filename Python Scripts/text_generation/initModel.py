import torch
from transformers import BitsAndBytesConfig
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding

def init_llama():
    system_prompt ='''You are a helpful, respectful, and honest medical assistant. Always answer as helpfully as possible while being
                      safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal
                      content. Please ensure that your responses are socially unbiased and positive in nature.
                      If a question does not make any sense, or is not factually coherent, explain why instead of answering
                      something not correct. If you don't know the answer to a question, please don't share false information.'''
    query_wrapper_prompt = PromptTemplate('<|USER|>{query_str}<|ASSISTANT|>')
    llm = HuggingFaceLLM(
    context_window = 4096,
    max_new_tokens = 100,
    generate_kwargs={'temperature' : 0.0, 'do_sample': False},
    system_prompt = system_prompt,
    query_wrapper_prompt = query_wrapper_prompt,
    tokenizer_name = 'AdaptLLM/medicine-chat',
    model_name = 'AdaptLLM/medicine-chat',
    device_map = 'auto',
    model_kwargs = {'torch_dtype': torch.float16, 'quantization_config' : BitsAndBytesConfig(load_in_8bit = True) }   
)

    return llm

def init_embedding_model():
    embedding_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2'))
    return embedding_model
