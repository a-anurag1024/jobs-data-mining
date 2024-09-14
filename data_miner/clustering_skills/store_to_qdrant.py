from sentence_transformers import SentenceTransformer
from dataclasses import dataclass 
from pathlib import Path

from data_miner.db.top_skills import DB_Creds, TopSkillsTable
from data_miner.db.qdrant import QdrantConfig, TopSkillsPayload, VectorDB

@dataclass
class StoreEMBs_Args:
    
    sql_db_creds: DB_Creds
    qdrant_config: QdrantConfig

    model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'
    model_cache_dir: str = Path("C:\\Users\\aanur\\projects\\jobs-data-mining\\mount\\all-MiniLM-L6-v2")
    
    
class StoreEMBs:
    def __init__(self, args: StoreEMBs_Args):
        self.args = args
        self.model = SentenceTransformer(self.args.model_name, cache_folder=self.args.model_cache_dir)
        self.vector_db = VectorDB(self.args.qdrant_config)
        self.top_skills_table = TopSkillsTable(self.args.sql_db_creds)
        
    
    def update_vector_db(self):
        return NotImplementedError