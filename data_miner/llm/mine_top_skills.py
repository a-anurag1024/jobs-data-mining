from typing import List
import re
import json

from data_miner.llm.processor import Processor, ProcessorConfig

from data_miner.db.top_skills import TopSkillsTable, DB_Creds
from data_miner.db.jobs import JobsTable



class TopSkillsMiner(Processor):
    def __init__(self, 
                 config: ProcessorConfig,
                 db_creds: DB_Creds):
        self.top_skills_table = TopSkillsTable(db_creds)
        self.jobs_table = JobsTable(db_creds)
        self.completed_jobs = self.top_skills_table.get_all_job_ids()
        super().__init__(config)
        
        
    def get_run_input_objects(self) -> List[dict]:
        
        job_ids = self.jobs_table.get_all_job_ids()
        data_objects = []
        for job_id in job_ids:
            if job_id in self.completed_jobs:
                continue
            jd = self.jobs_table.get_job_data(job_id, ["job_description"])["job_description"]
            data_objects.append({
                "job_id": job_id,
                "description": jd,
            })
        return data_objects
    
    
    def retrieve_info_from_results(self, result: str) -> dict:
        
        try:
            pattern = r"\n\s*\d+\.\s*([^\n]+)"
            top_skills = re.findall(pattern, result)
            assert len(top_skills) <110, "The number of top skills is more than 10"
            assert len(top_skills) > 0, f"The number of top skills is less than 1"
        except:
            print(f"Result: {result}")
            raise ValueError("The result is not as expected")
        
        return {
            "top_skills": "#".join(top_skills),
            "number_of_skills": len(top_skills),
            "exact_llm_output": result
        }