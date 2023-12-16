import streamlit as st
import pyodbc
import psutil

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

# Function to get basic monitoring metrics
def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Streamlit app
def main():
    st.title("Database Backend Monitoring App")

    # Connect to the database
    connection = db_connect()

    if connection:
        st.success("Connected to the database.")

        # Display basic database metrics
        st.header("Database Metrics")

        # Example 1: Get the number of records in dbo.Fact_Finhub1
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.Fact_Finhub1")
        result = cursor.fetchone()
        st.write(f"Number of records in dbo.Fact_Finhub1: {result[0]}")
        cursor.close()

        # Example 2: Get the total data volume in dbo.Fact_Finhub1
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(DATALENGTH(*)) FROM dbo.Fact_Finhub1")
        result = cursor.fetchone()
        total_data_volume = result[0] / (1024 * 1024)  # Convert to megabytes
        st.write(f"Total data volume in dbo.Fact_Finhub1: {total_data_volume:.2f} MB")
        cursor.close()

        # Example 3: Get the number of databases (dbo)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME LIKE 'dbo'")
        result = cursor.fetchone()
        st.write(f"Number of databases (dbo): {result[0]}")
        cursor.close()

        # Display KPI cards for system metrics
        st.header("System Metrics")

        # Get system metrics
        cpu_usage, memory_usage = get_system_metrics()

        # Display CPU usage as a KPI card
        st.metric(label="CPU Usage", value=f"{cpu_usage}%", delta=cpu_usage)

        # Display memory usage as a KPI card
        st.metric(label="Memory Usage", value=f"{memory_usage}%", delta=memory_usage)

        # Close the database connection
        connection.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    main()
