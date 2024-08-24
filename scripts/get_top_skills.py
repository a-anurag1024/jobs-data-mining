from pathlib import Path

from data_miner.llm.mine_top_skills import TopSkillsMiner
from data_miner.llm.processor import ProcessorConfig
from data_miner.llm.langchain_ollama import LangChain_config

from data_miner.db.top_skills import DB_Creds

def get_top_skills():
    
    langchain_config = LangChain_config(config_path=str(Path("../llm_configs/top_skills_miner.json")))
    
    config = ProcessorConfig(
        run_name="top_skills_miner",
        save_folder=str(Path("../mount/top_skills/processed")),
        log_folder=str(Path("../mount/top_skills/logs")),
        langchain_config=langchain_config,
        max_wait_time=60
    )
    
    db_creds = DB_Creds(
        host="localhost",
        port="3306",
        user="local",
        password="local",
        database="jobs_data"
    )
    
    top_skills_miner = TopSkillsMiner(config, db_creds)
    
    
    # Run the processor
    top_skills_miner.run()
    
    
if __name__ == "__main__":
    
    get_top_skills()