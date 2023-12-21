import streamlit as st
import pyodbc
import psutil
import pandas as pd

# Set the theme to light
st.set_theme("light")

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
    st.title("OpenDI Hackathon Mini Data Cloud")

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
        SELECT TOP 10
            r.creation_time,
            s.text AS [SQL Text],
            r.total_elapsed_time / 1000.0 AS [Total Elapsed Time (s)],
            r.total_worker_time / 1000.0 AS [Total Worker Time (s)],
            r.execution_count,
            r.plan_handle
        FROM
            sys.dm_exec_query_stats r
        CROSS APPLY
            sys.dm_exec_sql_text(r.sql_handle) s
        ORDER BY
            r.creation_time DESC;
        """
        results = execute_sql_query(connection, sql_query)

        # Display SQL query results in a table
        if results is not None:
            st.header("SQL Query Results")
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
