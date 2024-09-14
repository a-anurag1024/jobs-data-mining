from pathlib import Path

from data_miner.clustering_skills.create_clusters import ClusterConfig, ClusterSkills
from data_miner.db.top_skills import DB_Creds

def main():
        
    db_creds = DB_Creds(
        host="localhost",
        port="3306",
        user="local",
        password="local",
        database="jobs_data"
    )
    
    config = ClusterConfig(
        db_creds=db_creds,
        num_of_dimensions=25,
        num_of_clusters=38,
        embeddings_path=Path('../mount/top_skills_embeddings/embeddings.npy'),
        embeddings_metadata=Path('../mount/top_skills_embeddings/metadata.json'),
        wordcloud_save_dir=Path('../mount/top_skills_wordclouds'),
        wordcloud_threshold=0.4,
        skill_group_tagger_config=Path('../llm_configs/skill_cluster_namer.json'),
        run_save_dir=Path('../mount/skill_clustering_run_details')
    )
    
    cluster_skills = ClusterSkills(config)
    cluster_skills.run()
    
    
if __name__ == "__main__":
    
    main()