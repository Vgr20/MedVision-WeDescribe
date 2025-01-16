from typing_extensions import Text
from initModel import init_llama, init_embedding_model
from queryFunction import query_engine_object
from questionExtract import prompt_list
from tqdm import tqdm
import argparse
import os
import json

# pipeline object
class TextGenerationPipeline(object):
    
    def __init__(self):
        self.llm = init_llama()
        self.embedding_model = init_embedding_model()
        self.query_engine = query_engine_object(self.llm,self.embedding_model)
    
    def generation(self, prompt_dict):
        attr_dict = {}
        keys = list(prompt_dict.keys())
        for i in tqdm(range(len(keys)),desc="Text Generation", leave = False):
            answer = self.query_engine.query(prompt_dict[keys[i]])
            attr_dict[keys[i]] = answer.response
        return attr_dict

if __name__ == "__main__":
  # giving argument 
  parser = argparse.ArgumentParser(description="Text Generation using Med_Llama_2 ")
  parser.add_argument("--path", help="Path of the csv file", required=True)
  args = parser.parse_args()
  table_path = args.path

  table_name = os.path.basename(table_path)

  # pipline initiation
  pipeline = TextGenerationPipeline()

  # prompt extraction
  prompt_dict = prompt_list(table_path)

  # text generation
  answer_dict = pipeline.generation(prompt_dict)

  # json file creation
  json_path = f'/content/drive/MyDrive/Colab_Notebooks/IEEE_IES_Generative_AI_Hackathon/Testing_Pipeline/outputs/text_gen_{table_name[:-12]}.json'
  with open(json_path, "w") as json_file:
    json.dump(answer_dict, json_file)
