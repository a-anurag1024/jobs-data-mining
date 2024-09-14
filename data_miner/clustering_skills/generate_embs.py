from sentence_transformers import SentenceTransformer
from dataclasses import dataclass 
from pathlib import Path
import numpy as np
import json
from tqdm import tqdm

from data_miner.db.top_skills import DB_Creds, TopSkillsTable

@dataclass
class GenEmb_Args:
    
    db_creds: DB_Creds
    save_dir: Path
    
    model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'
    model_cache_dir: str = Path("C:\\Users\\aanur\\projects\\jobs-data-mining\\mount\\all-MiniLM-L6-v2")
    
    
    def __post_init__(self):
        self.save_dir.mkdir(parents=True, exist_ok=True)
    
    
class GenEmb:
    def __init__(self, args: GenEmb_Args):
        self.args = args
        self.model = SentenceTransformer(self.args.model_name, cache_folder=self.args.model_cache_dir)
        self.top_skills_table = TopSkillsTable(self.args.db_creds)
        
        self.embeddings = np.array([])
        self.index = 0
        self.metadata = []
    
    
    def save_to_file(self):
        np.save(self.args.save_dir / "embeddings.npy", self.embeddings)
        with open(self.args.save_dir / "metadata.json", "w") as f:
            json.dump(self.metadata, f, indent=4)
    
    
    def generate_embeddings(self):
        jobs = self.top_skills_table.get_all_top_skills()
        for job in tqdm(jobs.iloc[:].itertuples(), total=jobs.shape[0], desc="Generating embeddings"):
            skills = job.top_skills.split("#")
            for j, skill in enumerate(skills):
                emb = self.model.encode(skill)
                if self.embeddings.shape[0] == 0:
                    self.embeddings = emb.reshape(1, -1)
                else:
                    self.embeddings = np.append(self.embeddings, emb.reshape(1, -1), axis=0)
                self.metadata.append({
                    "job_id": job.job_id,
                    "array_index": self.index,
                    "skill": skill,
                    "skill_rank": j+1
                })
                self.index += 1
            self.save_to_file()