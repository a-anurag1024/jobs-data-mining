from data_miner.db.base_table import BaseTable, DB_Creds


class SkillsClusterTagTable(BaseTable):
    def __init__(self, db_creds: DB_Creds):
        super().__init__(db_creds)
        
        
    @property
    def table_name(self):
        return "skills_cluster_tag"
    
    
    def _create_table(self) -> None:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name}(
            id INT AUTO_INCREMENT PRIMARY KEY,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            job_id VARCHAR(256),
            skill VARCHAR(10000),
            skill_rank INT,
            cluster_id VARCHAR(2560)
        )
        """
        
        self.db.cursor().execute(create_table_query)
        self.db.commit()
        
        
    def delete_all_data(self):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM {self.table_name}")
        self.db.commit()