# Import libraries required for connecting to mysql
import mysql.connector
# Import libraries required for connecting to DB2 or PostgreSql
import ibm_db
# Connect to MySQL
connection = mysql.connector.connect(user='root', password='OTczNy1tb2hhbWVk',host='127.0.0.1',database='sales')
cursor = connection.cursor()
# Connect to DB2 or PostgreSql
dsn_hostname = "ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "pql88073"        # e.g. "abc12345"
dsn_pwd = "1gJmyQwxMGqqc0G9"      # e.g. "7dBZ3wWt9XN6$o0J"
dsn_port = "31321"                # e.g. "50000" 
dsn_database = "bludb"            # i.e. "BLUDB"
dsn_driver = "{IBM DB2 ODBC DRIVER}" # i.e. "{IBM DB2 ODBC DRIVER}"           
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"              # i.e. "SSL"


dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)


conn = ibm_db.connect(dsn, "", "")
print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    last_rowid_sql = 'SELECT rowid FROM sales_data ORDER BY rowid DESC LIMIT 1'
    last_rowid_stmt = ibm_db.exec_immediate(conn, last_rowid_sql)
    while ibm_db.fetch_row(last_rowid_stmt) != False:
        return ibm_db.result(last_rowid_stmt, 0)

last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    latest_records_sql = f'SELECT * FROM sales_data WHERE rowid > {last_row_id} ORDER BY rowid ASC'
    cursor.execute(latest_records_sql)
    return cursor.fetchall()	

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
    insert_sql = "INSERT INTO sales_data (rowid, product_id, customer_id, quantity) VALUES (?,?,?,?);"
    insert_stmt = ibm_db.prepare(conn, insert_sql)
    for row in records:
        ibm_db.execute(insert_stmt, row)


insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()
# disconnect from DB2 or PostgreSql data warehouse 
ibm_db.close(conn)
# End of program