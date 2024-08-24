from dataclasses import dataclass, field 
from typing import List, Tuple
import json

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.llms import OllamaLLM

@dataclass
class LangChain_config:
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_prompt = [
            ("human", "generate the output as per the schema: {schema}"),
            ("human", "Keep the output very short and concise")
        ]
        self._set_config()
        
        
    def _set_config(self):
        self.config = json.load(open(self.config_path, "r"))
        self.system_prompts = [tuple(sp) for sp in self.config["system_prompts"]]
        self.output_schema = self.config["output_schema"]
    
    
    
    @property
    def prompts(self):
        return self.system_prompts + self.default_prompt
    
    
    
    

class LangChainPipeline:
    def __init__(self, config: LangChain_config):
        
        self.config = config
        self.prompt = self._set_prompt()
        self.model = OllamaLLM(model="llama3")
        self.chain = self.prompt | self.model
        
        
    def _set_prompt(self):
        return ChatPromptTemplate.from_messages(self.config.prompts)
    
    def run(self, inputs: str):
        return self.chain.invoke({**inputs, 
                                  "schema": self.config.output_schema}
                                 )