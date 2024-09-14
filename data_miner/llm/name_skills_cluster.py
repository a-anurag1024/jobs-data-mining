import re 
from typing import List

from data_miner.llm.langchain_ollama import LangChainPipeline, LangChain_config


class SkillGroupTagger(LangChainPipeline):
    def __init__(self, 
                 config_path: str,
                 max_retries: int = 5):
        config = LangChain_config(config_path)
        super().__init__(config)
        
        self.max_retries = max_retries
        
        
    def _result_validator(self, result: str):
        try:
            pattern = r"Tag:\s*(.+)"
            match = re.search(pattern, result, re.IGNORECASE)
            skill_group_tag = match.group(1)
        except:
            print(f"Result: {result}")
            raise ValueError("The result is not as expected")
        
        return skill_group_tag
        
        
    def tag(self, top_skills: List[str]):
        inputs = {
            "skills": ", ".join(top_skills)
        }
        retries=0
        while retries < self.max_retries:
            try:
                result = self.run(inputs)
                return self._result_validator(result)
            except:
                retries += 1