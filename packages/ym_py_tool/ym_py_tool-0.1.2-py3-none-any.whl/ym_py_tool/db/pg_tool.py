import psycopg2
from psycopg2 import sql
from typing import Callable
import uuid


class PostgreSQLTool:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        """
        初始化数据库连接参数
        :param dbname: 数据库名称
        :param user: 用户名
        :param password: 密码
        :param host: 主机地址，默认为 'localhost'
        :param port: 端口号，默认为 5432
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        进入上下文时自动连接数据库
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
            return self
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文时自动关闭数据库连接
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is not None:  # 如果有异常，回滚事务
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """
        执行 SQL 查询
        :param query: SQL 查询语句
        :param params: 查询参数，默认为 None
        :return: 查询结果
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def execute_query_dict(self, query, params=None):
        """
        执行 SQL 查询,返回字典列表
        :param query: SQL 查询语句
        :param params: 查询参数，默认为 None
        :return: 查询结果
        """
        try:
            # 获取列名
            self.cursor.execute(query, params)
            column_names = [desc[0] for desc in self.cursor.description]
            return [dict(zip(column_names, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def execute_stream_query(
        self, query, params=None, call_back: Callable = None, chunk_size=1000
    ):
        """
        执行 SQL 流式查询
        :param query: SQL 查询语句
        :param params: 查询参数，默认为 None
        :param call_back: 回调函数
        :param chunk_size: 块大小
        """
        unique_id = uuid.uuid4().hex
        try:
            if self.cursor:
                self.cursor.close()
            # 必须要为游标命名,不然流式读取不生效
            self.cursor = self.connection.cursor(unique_id)

            self.cursor.execute(query, params)

            while True:
                result = self.cursor.fetchmany(chunk_size)  # 每次读取 1000 条数据
                if not result:  # 如果 result 是空列表，退出循环
                    break
                call_back(result)  # 处理数据
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def execute_insert(self, table, data):
        """
        插入数据到指定表
        :param table: 表名
        :param data: 要插入的数据，字典形式
        """
        columns = data.keys()
        values = [data[column] for column in columns]
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(map(sql.Placeholder, columns)),
        )
        try:
            self.cursor.execute(query, values)
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise
