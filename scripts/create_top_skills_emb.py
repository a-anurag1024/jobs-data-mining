from pathlib import Path 

from data_miner.db.top_skills import DB_Creds
from data_miner.clustering_skills.generate_embs import GenEmb, GenEmb_Args


def main():
    
    db_creds = DB_Creds(
        host="localhost",
        port="3306",
        user="local",
        password="local",
        database="jobs_data"
    )
    
    args = GenEmb_Args(
        db_creds=db_creds,
        save_dir=Path("C:\\Users\\aanur\\projects\\jobs-data-mining\\mount\\top_skills_embeddings")
    )
    
    gen_emb = GenEmb(args)
    gen_emb.generate_embeddings()
    
    
if __name__ == "__main__":
    
    main()