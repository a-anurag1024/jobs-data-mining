from abc import ABC, abstractmethod 
from dataclasses import dataclass 
import pandas as pd

import mysql.connector as mysql

@dataclass
class DB_Creds:
    
    host: str
    port: str
    user: str
    password: str
    database: str
    

class BaseTable(ABC):
    def __init__(self, db_creds: DB_Creds):
        
        self.__creds = db_creds
        self._connect()
        
        self._create_table()
        
        
    def _connect(self) -> None:
        self.db = mysql.connect(
            host=self.__creds.host,
            port=self.__creds.port,
            user=self.__creds.user,
            password=self.__creds.password,
            database=self.__creds.database
        )
        
        
    @property 
    @abstractmethod
    def table_name(self):
        pass
    
    
    @abstractmethod
    def _create_table(self) -> None:
        """
        Define the table to be created here. 
        Also execute the CREATE TABLE command using the connector self.db
        
        WARNING:- Only Create the table if it does not exist
        """
        pass
    
    
    def insert_data(self, data: dict) -> None:
        """
        Insert the data into the table
        
        Args:
            data: dict
                The data to be inserted into the table. The keys of the dict should be the columns of the table
        
        Returns:
            None
        """
        cursor = self.db.cursor()
        entry_tags = list(data.keys())
        command = f"""INSERT INTO {self.table_name} ({', '.join(entry_tags)})"""
        command += f" VALUES ({', '.join(['%s' for _ in range(len(entry_tags))])})"
        values = [data[tag] for tag in entry_tags]
        cursor.execute(command, values)
        self.db.commit()
        cursor.close()
    
    
    def select_all(self) -> pd.DataFrame:
        
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        data = cursor.fetchall()
        cursor.close()
        
        return pd.DataFrame(data, columns=[i[0] for i in cursor.description])