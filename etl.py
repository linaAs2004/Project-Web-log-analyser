
import mysql.connector 
import re
import logging
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        user='root',
        passwd='',
        host='localhost',
        port=3306,
        database='dblog'  
    )

logging.basicConfig(filename='secure', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
Ch = logging.StreamHandler()
Ch.setLevel(logging.INFO)  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
Ch.setFormatter(formatter)
logging.getLogger().addHandler(Ch)

def extract_ssh_logs(path):
    pattern = r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\ssshd\[(\d+)\]:\s(.+)$'
    data = []

    with open(path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                groups = match.groups()
                timestamp_str = groups[0]
                timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
                timestamp = timestamp.replace(year=datetime.now().year)
                data.append({
                    'log_date': timestamp.strftime('%Y-%m-%d'),
                    'log_time': timestamp.strftime('%H:%M:%S'),
                    'pid': int(groups[2]),
                    'message': groups[3],
                    'ip_address': groups[1]
                })
    return data

def extract_apache_access_logs(path):
    pattern = r'(\S+) \S+ \S+ \[(.+?)\] "(\w+) (.+?) HTTP/1.\d" (\d+) \d+ ".*" "(.*)"'
    data = []

    with open(path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                groups = match.groups()
                timestamp_str = groups[1]
                timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S %z')
                data.append({
                    'ip_address': groups[0],
                    'timestamp': timestamp,
                    'requested_resource': groups[3],
                    'static_request': groups[2],
                    'status_code': int(groups[4]),
                    'user_agent': groups[5]
                })
    return data

def extract_apache_error_logs(path):
    pattern = r"\[(.*?)\] \[([^\]]+)\] \[pid (\d+)\] (.*)"
    data = []

    with open(path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                groups = match.groups()
                timestamp_str = groups[0]
                try:
                    timestamp_match = re.search(r'^[a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{6} \d{4}', timestamp_str)
                    if timestamp_match:
                        clean_timestamp_str = timestamp_match.group(0)
                        timestamp = datetime.strptime(clean_timestamp_str, '%a %b %d %H:%M:%S.%f %Y')
                        data.append({
                            'log_time': timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
                            'log_level': groups[1],
                            'pid': int(groups[2]),
                            'message': groups[3]
                        })
                    else:
                        logging.error(f"Timestamp format not recognized: {timestamp_str}")
                except (ValueError, AttributeError) as ve:
                    logging.error(f"Error parsing timestamp: {timestamp_str} with error {ve}")
    return data

def existe_DB(database: str, cursor) -> bool:
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    for db in databases:
        if db[0] == database:
            return True
    return False

def existe_table(table_name, cursor):
    try:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        return bool(result)
    except mysql.connector.Error as error:
        logging.error(f"Error: {error}")
        return False

def load_ssh_logs(data, cursor):
    try:
        if not existe_table('ssh_logs', cursor):
            cursor.execute("""
                CREATE TABLE ssh_logs (
                    log_date DATE,
                    log_time TIME,
                    pid INT,
                    message TEXT,
                    hostname VARCHAR(255)
                )
            """)
            logging.info("Table 'ssh_logs' created successfully.")
        
        for log in data:
            cursor.execute("""
                INSERT INTO ssh_logs (log_date, log_time, pid, message, hostname)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                log['log_date'],
                log['log_time'],
                log['pid'],
                log['message'],
                log['hostname']
            ))
        cursor.execute("COMMIT")
        logging.info("Data inserted into 'ssh_logs' table successfully.")
    except mysql.connector.Error as error:
        logging.error(f"Error: {error}")

def load_apache_access_logs(data, cursor):
    try:
        if not existe_table('apache_access_logs', cursor):
            logging.info("Creating table 'apache_access_logs'")
            cursor.execute("""
                CREATE TABLE apache_access_logs (
                    ip_address VARCHAR(255),
                    timestamp DATETIME,
                    requested_resource TEXT,
                    static_request VARCHAR(10),                                                                                                        
                    status_code INT,
                    user_agent TEXT
                )
            """)
            logging.info("Table 'apache_access_logs' created successfully.")

        for entry in data:
            raw_timestamp = entry['timestamp']
            formatted_timestamp = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT INTO apache_access_logs (ip_address, timestamp, requested_resource, static_request, status_code, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entry['ip_address'],
                formatted_timestamp,
                entry['requested_resource'],
                entry['static_request'],
                entry['status_code'],
                entry['user_agent']
            ))
        cursor.execute("COMMIT")
        logging.info("Data inserted into 'apache_access_logs' table successfully.")
    except mysql.connector.Error as error:
        logging.error(f"Error: {error}")

def load_apache_error_logs(data, cursor):
    try:
        if not existe_table('apache_error_logs', cursor):
            cursor.execute("""
                CREATE TABLE apache_error_logs (
                    log_time DATETIME,
                    log_level VARCHAR(255),
                    pid INT,
                    message TEXT
                )
            """)
            logging.info("Table 'apache_error_logs' created successfully.")

        for entry in data:
            cursor.execute("""
                INSERT INTO apache_error_logs (log_time, log_level, pid, message)
                VALUES (%s, %s, %s, %s)
            """, (
                entry['log_time'],
                entry['log_level'],
                entry['pid'],
                entry['message']
            ))
        cursor.execute("COMMIT")
        logging.info("Data inserted into 'apache_error_logs' table successfully.")
    except mysql.connector.Error as error:
        logging.error(f"Error: {error}")

if __name__ == '__main__':
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Load SSH logs
        ssh_path = 'C:/Users/HP/Desktop/Project-Web-log-analyser/DATA/Logs/secure-20220313'
        ssh_data = extract_ssh_logs(ssh_path)
        ssh_data_dict = {'ssh_logs': ssh_data}
        #print(ssh_data_dict)

        # Load Apache access logs
        apache_access_path = 'C:/Users/HP/Desktop/Project-Web-log-analyser/DATA/Logs/access_log'
        apache_access_data = extract_apache_access_logs(apache_access_path)
        apache_access_data_dict = {'apache_access_logs': apache_access_data}
        #print(apache_access_data_dict)

        # Load Apache error logs
        apache_error_path = 'C:/Users/HP/Desktop/Project-Web-log-analyser/DATA/Logs/error_log'
        apache_error_data = extract_apache_error_logs(apache_error_path)
        apache_error_data_dict = {'apache_error_logs': apache_error_data}
        #print(apache_error_data_dict)

        #load_ssh_logs(ssh_data_dict['ssh_logs'], cursor)  
        load_apache_access_logs(apache_access_data, cursor)  
        #load_apache_error_logs(apache_error_data, cursor) 

    except mysql.connector.Error as e:
        logging.error("Error while connecting to MySQL server: %s", e)
