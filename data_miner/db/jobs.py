from data_miner.db.base_table import BaseTable, DB_Creds


class JobsTable(BaseTable):
    def __init__(self, db_creds: DB_Creds):
        super().__init__(db_creds)
        
        
    @property
    def table_name(self):
        return "jobs"
    
    
    @property
    def fields(self):
        return ["entry_date", "job_id", "job_link", "job_description", "seniority_level", "employment_type", "job_function", "industries"]
    
    
    def _create_table(self) -> None:
        cursor = self.db.cursor()
        command = """
        CREATE TABLE IF NOT EXISTS jobs(
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            job_id VARCHAR(255) PRIMARY KEY,
            job_link VARCHAR(2555),
            job_description TEXT,
            seniority_level VARCHAR(255),
            employment_type VARCHAR(255),
            job_function VARCHAR(255),
            industries VARCHAR(255)
            )
            """
        cursor.execute(command)
        self.db.commit()
        cursor.close()
        
        
    def get_all_job_ids(self) -> list:
        cursor = self.db.cursor()
        command = f"SELECT job_id FROM {self.table_name}"
        cursor.execute(command)
        data = cursor.fetchall()
        cursor.close()
        return [d[0] for d in data]
    
    
    def get_job_data(self, 
                     job_id: str, 
                     fields: list) -> dict:
        """
        Get the data for a job_id
        
        Args:
            job_id: str
                The job_id for which the data is to be fetched
            fields: list
                The fields to be fetched for the job_id. check self.fields for the available fields
        """
        cursor = self.db.cursor()
        attributes = ", ".join(fields)
        command = f"SELECT {attributes} FROM {self.table_name} WHERE job_id = '{job_id}'"
        cursor.execute(command)
        data = cursor.fetchall()[0]
        cursor.close()
        data = {fields[i]: data[i] for i in range(len(fields))}
        return data