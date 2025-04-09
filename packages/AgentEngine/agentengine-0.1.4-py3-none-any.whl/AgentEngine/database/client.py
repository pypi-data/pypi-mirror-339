import os
import psycopg2
import psycopg2.extras
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class PostgresClient:
    _instance: Optional['PostgresClient'] = None
    _conn: Optional[psycopg2.extensions.connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST', 'localhost')
        self.user = os.getenv('POSTGRES_USER', 'user_name')
        self.password = os.getenv('POSTGRES_PASSWORD', 'user_password')
        self.database = os.getenv('POSTGRES_DB', 'agent_engine')
        self.port = os.getenv('POSTGRES_PORT', 5432)

    def get_connection(self):
        """获取数据库连接"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                dbname=self.database,
                port=self.port
            )
            return conn
        except Exception as e:
            raise Exception(f"数据库连接失败: {str(e)}")

    def close_connection(self, conn):
        """关闭数据库连接"""
        if conn:
            conn.close()

    def clean_string_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """确保所有字符串都是UTF-8编码"""
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = value.encode('utf-8', errors='ignore').decode('utf-8')
            else:
                cleaned_data[key] = value
        return cleaned_data

# 创建一个全局的数据库客户端实例
db_client = PostgresClient()
