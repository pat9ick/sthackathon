import streamlit as st
import pyodbc
import psutil
import pandas as pd

# Function to connect to the database
def db_connect():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=database-hackathon.cfn2vvgqdwd8.ap-southeast-2.rds.amazonaws.com,1433;'
            'DATABASE=Hackathon;'
            'UID=admin;'
            'PWD=Hackathon2023db;'
            'TrustServerCertificate=yes'
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to execute SQL query and return results as a DataFrame
def execute_sql_query(connection, sql_query):
    try:
        result = pd.read_sql_query(sql_query, connection)
        return result
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return None

# Function to get basic monitoring metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Function to create a performance gauge chart
def performance_gauge_chart(percentage):
    # Display a progress bar to represent the performance
    st.subheader("Performance Gauge Chart")
    st.progress(percentage / 100)

    # Display the percentage value
    st.write(f"Performance: {percentage}%")

# Streamlit app
def main():
    st.title(" :cd: OpenDI Hackathon Mini Data Cloud")

    # Display basic system metrics
    st.header("System Metrics")

    # Get system metrics
    cpu_usage, memory_usage = get_system_metrics()

    # Create and display CPU usage gauge
    st.subheader("CPU Usage")
    st.progress(cpu_usage / 100)
    st.write(f"CPU Usage: {cpu_usage}%")

    # Create and display Memory usage gauge
    st.subheader("Memory Usage")
    st.progress(memory_usage / 100)
    st.write(f"Memory Usage: {memory_usage}%")

    # Display Performance Gauge Chart
    # performance_gauge_chart(75)  # Replace 75 with your actual performance percentage

    # Connect to the database
    connection = db_connect()

    if connection:
        st.success("Connected to the database.")

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

        # Display SQL query results in a table
        if results is not None:
            st.header("Wait Stats")
            st.dataframe(results)
        else:
            st.warning("No results to display.")

        # Close the database connection

        # Display connection string
        st.header("Connection String")
        st.markdown(
            '''
            The connection string to the database is:
            ```
            DRIVER={ODBC Driver 17 for SQL Server};
            SERVER=database-hackathon.cfn2vvgqdwd8.ap-southeast-2.rds.amazonaws.com,1433;
            DATABASE=Hackathon;
            UID=admin;
            PWD=************;
            TrustServerCertificate=yes
            ```
            '''
        )

        connection.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    main()
