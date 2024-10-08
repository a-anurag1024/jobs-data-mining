from data_miner.db.base_table import BaseTable, DB_Creds
import pandas as pd

class TopSkillsTable(BaseTable):
    def __init__(self, db_creds: DB_Creds):
        super().__init__(db_creds)
        
        
    @property
    def table_name(self):
        return "top_skills"
    
    
    def _create_table(self) -> None:
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name}(
            id INT AUTO_INCREMENT PRIMARY KEY,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            job_id VARCHAR(256),
            top_skills VARCHAR(10000),
            number_of_skills INT,
            exact_llm_output TEXT
        )
        """
        
        self.db.cursor().execute(create_table_query)
        self.db.commit()
        
        
    def get_all_job_ids(self) -> list:
        cursor = self.db.cursor()
        command = f"SELECT job_id FROM {self.table_name}"
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return [d[0] for d in data]
    
    
    def get_all_top_skills(self) -> pd.DataFrame:
        cursor = self.db.cursor()
        command = f"SELECT * FROM {self.table_name}"
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return pd.DataFrame(data, columns=[d[0] for d in cursor.description])