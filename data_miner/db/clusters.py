from data_miner.db.base_table import BaseTable, DB_Creds
import pandas as pd

class SkillsClustersTable(BaseTable):
    def __init__(self, db_creds: DB_Creds):
        super().__init__(db_creds)
        
        
    @property
    def table_name(self):
        return "skills_clusters"
    
    
    def _create_table(self) -> None:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name}(
            id INT AUTO_INCREMENT PRIMARY KEY,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cluster_id INT,
            cluster_tags TEXT,
            cluster_head_tag VARCHAR(1000)
        )
        """
        
        self.db.cursor().execute(create_table_query)
        self.db.commit()
        
        
    def delete_all_data(self):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM {self.table_name}")
        self.db.commit()