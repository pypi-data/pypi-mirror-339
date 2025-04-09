import json
import snowflake.connector as snowflake
import os
import sys
import datetime

import logging

class DB:
    def __init__(self):
        self.working_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            self.db_config = self.load_db_config()
        except Exception as e:
            raise Exception(f"DB - An error occurred while loading the database configuration: {e}")
    def load_db_config(self) -> dict:
        config_file = os.path.join(self.working_dir, 'db_config.json')

        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    def get_db_config(self) -> dict:
        return self.db_config



class Snowflake(DB):

    def __init__(self):
        try:
            super().__init__()
        except Exception as e:
            raise Exception(e)
        from pathlib import Path
        home = Path.home()

        sys.path.append(home)
        log_dir = os.path.join(home, "rusta_logs")

        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating log directory: {e}")
            SystemExit(1)

        log_file = os.path.join(log_dir, f"spider log {datetime.date.today().strftime('%Y-%m-%d')}.log")
        self.logger = logging.getLogger(__name__)
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def get_pwd(self):
        from cryptography.fernet import Fernet
        from pathlib import Path
        home = Path.home()

        sys.path.append(home)
        settings_dir = os.path.join(home, "rusta_crawler_settings")
        path = os.path.join(settings_dir, 'key.json')
        with open(path, 'r') as file:
            key = json.load(file)

        key = key['fernet_key']
        
        f = Fernet(key)
        password = self.db_config['snowflake_rusta_dwh']['password']
        decpwd = f.decrypt(password).decode('utf-8')
        return decpwd
        
        
    def connect_to_snowflake(self, dwh):
        # Establish a connection to get campaign data
        try:
            pwd = self.get_pwd()
            if dwh == 'CAMPAIGN_VERIFICATION':
                self.conn = snowflake.connect(
                    account=self.db_config['snowflake_rusta_dwh']['account'],
                    user=self.db_config['snowflake_rusta_dwh']['user'],
                    password=pwd,
                    warehouse=self.db_config['snowflake_rusta_dwh']['warehouse'],
                    database=self.db_config['snowflake_rusta_dwh']['database'],
                    schema=self.db_config['snowflake_rusta_dwh']['schema'],
                    role=self.db_config['snowflake_rusta_dwh']['role']
                )
            elif dwh == 'RUSTA_CRAWLER_DWH':
                self.conn = snowflake.connect(
                    account=self.db_config['snowflake_rusta_crawler_dwh']['account'],
                    user=self.db_config['snowflake_rusta_crawler_dwh']['user'],
                    password=pwd,
                    warehouse=self.db_config['snowflake_rusta_crawler_dwh']['warehouse'],
                    database=self.db_config['snowflake_rusta_crawler_dwh']['database'],
                    schema=self.db_config['snowflake_rusta_crawler_dwh']['schema'],
                    role=self.db_config['snowflake_rusta_crawler_dwh']['role']
                )

        except snowflake.errors.Error as e:
            sys.tracebacklimit = 0  
            raise snowflake.errors.Error("DB - An error occurred while connecting to Snowflake {e}")
        
    def close_snowflake_connection(self):
        self.conn.close()
        

    def get_data_from_db(self, query, dwh):
        self.connect_to_snowflake(dwh=dwh)
        rows = []
        b = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                rows.append(row[0])
            cursor.close()
            return rows
        except snowflake.errors.Error as e:
            sys.tracebacklimit = 0
            raise snowflake.errors.Error(f"DB - An error occurred while fetching data from Snowflake. Terminating execution: {e}")
        finally:
            self.close_snowflake_connection()
        
    def fetch_article_data(self, query, dwh):   
        self.connect_to_snowflake(dwh)
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)

            all_articles = []        
            results = cursor.fetchall()
            # print(len(results))
            for row in results:
                json_row = {}
                for i, column in enumerate(cursor.description):
                    json_row[column[0]] = row[i]
                    json_row
                all_articles.append(json_row)
            # Check if read is done
            if cursor.rowcount == len(all_articles):
                self.logger.info("DB - Read operation from completed successfully.")

            # Close the cursor
            cursor.close()
            # Close the connection
            self.close_snowflake_connection()
            return all_articles
        except snowflake.errors.Error as e:
            sys.tracebacklimit = 0
            raise snowflake.errors.Error(f"DB -An error occurred while fetching data from Snowflake. Terminating execution: {e}")

    
    def load_query(self, query_to_read):
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one directory level
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            query_dir = os.path.join(parent_dir, 'sql')
            query_file = os.path.join(os.path.join(query_dir, query_to_read))
            query = ""
            with open(query_file, 'r') as file:
                query = file.read()
            return query
        except Exception as e:
            raise Exception(f"DB - An error occurred while loading the query: {e}")
    

    def execute_query(self, query, dwh):
        self.connect_to_snowflake(dwh)
        result = None
        try:
            result = self.conn.cursor().execute(query).fetchall()
        except snowflake.errors.Error as e:
            sys.tracebacklimit = 0
            raise snowflake.errors.Error(f"DB - An error occurred while executing the query: {e}")
        finally:
            self.conn.cursor().close()
            self.close_snowflake_connection()
            self.logger.info("DB - Query executed successfully.")
            return result
    def build_sql_query(self, data, table_name):
        try:
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            return sql
        except Exception as e:
            raise Exception(f"DB - An error occurred while building the SQL query: {e}")
    def save_data_to_db(self, result, table_name):
        try:
            self.connect_to_snowflake('RUSTA_CRAWLER_DWH')
        
            if not result:
                self.logger.info("DB - No data to insert.")
                return
            
            # Build the SQL query using the first item in the result list
            query = self.build_sql_query(result[0], table_name)
            
            truncated_values = []
            for data in result:
                truncated_data = {k: (str(v)[:255] if isinstance(v, str) else v) for k, v in data.items()}
                truncated_values.append(list(truncated_data.values()))
            # Execute the bulk insert
            self.conn.cursor().executemany(query, truncated_values)
            self.conn.commit()
            self.logger.info("DB - Bulk write operation completed successfully for company: .")
        except snowflake.errors.Error as e:
            self.logger.info(f"DB - An error occurred while saving to Snowflake: {e}")  
            self.close_snowflake_connection()
            raise snowflake.errors.Error(f"DB - An error occurred while saving to Snowflake: {e}")
        except Exception as e:  
            self.close_snowflake_connection()
            raise Exception(f"DB - An error occurred while saving to Snowflake: {e}")
        finally:
            self.close_snowflake_connection()
        
    def delete_same_day_data(self, table_name, dwh, company=None, scrape_type=None):
        try:
            self.connect_to_snowflake(dwh)
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            sql = f"DELETE from  {table_name} where scrape_date = DATE '{date}'"
            if scrape_type:
                sql += f" and CAMPAIGN_PERIOD = '{scrape_type}'"
            if company:
                sql += f" and company = '{company}'"
            self.conn.cursor().execute(sql)
            self.close_snowflake_connection()
            self.logger.info(f"DB - Data deleted from Snowflake table: {table_name}")

        except snowflake.errors.Error as e:
            self.logger.error(f"DB - An error occurred while deleting from Snowflake: {e}")
            raise snowflake.errors.Error(f"DB - An error occurred while deleting from Snowflake: {e}")
