# Mini Cloud Data Project

Project description: implementation of mini data cloud with **minimum code and cost**.

Team Name: PRC

Members: @Riku, @Crazyrat, @Pat

Infra & language: AWS & Python/SQL

- [x] Part A WebSocket &ETL : A WebSocket source as an example, including a simple ETL processing the source data and load into the target database on AWS
- [x] Part B Frontend Dashboard based on open-source tool named Streamlit, including its native & free cloud hosting : [Streamlit (sthackathon-5swxdhgjb3brcvkutxi234.streamlit.app)](https://sthackathon-5swxdhgjb3brcvkutxi234.streamlit.app/) 
- [x] Part C Deployment: aws instance EC2 micro setup, aws database setup, SSH to connect to the instance



### Part A WebSocket & ETL 

Uses `websocket`,`json`,`pandas`,`pyodbc` python libraries as ETL tool

#### 1. Connect to DB

```python
def db_connect():
    return pyodbc.connect(
        '''
        Connection String
        '''
    )
```

#### 2. WebSocket Data (Extraction)

```python
if __name__ == "__main__":
    # Enabling WebSocket trace
    websocket.enableTrace(True)

    # Creating the WebSocketApp
    ws = websocket.WebSocketApp("""
    							WS String
    							""",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Running the WebSocketApp
    ws.run_forever()
```

#### 3. Field Mapping (Transform)

```python
def on_message(ws, message):
    msg = json.loads(message)

    if msg['type'] == 'trade':
        for data in msg['data']:
            original_data = {
                'type': msg['type'],
                'symbol': data['s'],
                'price': data['p'],
                'volume': data['v'],
                'timestamp': data['t']
            }
```

In this case the data is stock data so the type value needs no transform but the field name (e.g. abbreviation to whole name that defined in AWS database).

#### 4. Write DB (Load)

```python
def write_to_db(new_data):
    conn = db_connect()
    cursor = conn.cursor()
    
    # Construct the SQL INSERT query
    query = """
    INSERT INTO dbo.Fact_test1 (type, symbol, price, volume, timestamp) 
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (new_data['type'], new_data['symbol'], new_data['price'], new_data['volume'], new_data['timestamp']))
    
    conn.commit()
    cursor.close()
    conn.close()

```



### Dashboard

A `streamlit` cloud hosted app is applied in this project. `streamlit`,`pyodbc`,`psutil`(retrieve instance's information) and `pandas` python libraries are used when deploying the dashboard.![image-20231221141947940](https://github.com/pat9ick/sthackathon/blob/main/screenshot_streamlit.png?raw=true)

#### 1. Metrics to show 

```python
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage
```



#### 2. SQL to Monitor

```python
def execute_sql_query(connection, sql_query):
    try:
        result = pd.read_sql_query(sql_query, connection)
        return result
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return None
```

Here we use MS SQL's TSQL as an example to monitoring some wait stats, it can be any SQL, or db-native SQL (TSQL for example) depending on what db being used.

```sql
# Execute SQL query
sql_query = """
DECLARE @StartTime DATETIME = GETDATE();

SELECT 
    wait_type,
    waiting_tasks_count AS 'Waiting Tasks Count',
    wait_time_ms AS 'Total Wait Time (ms)',
    max_wait_time_ms AS 'Max Wait Time (ms)'
FROM 
    sys.dm_os_wait_stats
WHERE 
    waiting_tasks_count > 0
ORDER BY 
    waiting_tasks_count DESC;

PRINT 'Time Elapsed: ' + CONVERT(VARCHAR, DATEDIFF(MILLISECOND, @StartTime, GETDATE())) + ' ms';
PRINT '';

"""
results = execute_sql_query(connection, sql_query)
```

Example results as below:

![image-20231221143125725](https://github.com/pat9ick/sthackathon/blob/main/screenshot_waitstats.png?raw=true)



### Deployment & Run

AWS instance setting - EC2 (free tier)

**AWS CLI to create the instance**

```bash
aws configure

aws ec2 run-instances \
  --image-id ami-xxxxxxxxxxxxxxxxx \  # Replace with your AMI ID
  --instance-type t2.micro \
  --key-name YourKeyName \
  --security-groups YourSecurityGroup \
  --count 1
```

**Connect to the EC2 Instance:**

```bash
ssh -i YourKeyPair.pem ec2-user@your-instance-ip
```

Install SQL Server

```bash
sudo yum install -y mssql-tools
```

Connect to the db

```bash
sqlcmd -S your-rds-endpoint -U your-username -P your-password
```

Create the table (the example one)

```sql
CREATE TABLE [dbo].[Fact_Finhub1] (
    [type] NVARCHAR (50) NULL,
    [symbol] NVARCHAR (50) NULL,
    [price] FLOAT (53) NULL,
    [volume] FLOAT (53) NULL,
    [timestamp] BIGINT NULL
);
```

Once deployed, use below code via SSH to run the real-time data processing (below screenshot means the data application is running successfully)

```powershell
cd <path you keep the pem file (in github)>

ssh -i finhubaws.pem ubuntu@ec2-3-25-239-201.ap-southeast-2.compute.amazonaws.com
```

![image-20231221143125726](https://github.com/pat9ick/sthackathon/blob/b9dd1243fdb457c20f12b95d67e2c5e8c136eee5/screenshot_ssh.png?raw=true)
