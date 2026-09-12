import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

load_dotenv()

class Database:
    def __init__(self):
        self.server = os.getenv("DB_SERVER")
        self.database = os.getenv("DB_NAME")
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

    def get_engine(self):

        connection_url = URL.create(
            "mssql+pyodbc",
            username=self.username,
            password=self.password,
            host=self.server,
            port=1433,
            database=self.database,
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "Encrypt": "yes",
                "TrustServerCertificate": "no"
            }
        )
        
        engine = create_engine(connection_url,connect_args={"timeout": 30})
        return engine