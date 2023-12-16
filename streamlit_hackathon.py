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
            'PWD=XXXX;'
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
        # Add your SQL query here to fetch metrics from the database
        # Example: cursor = connection.cursor()
        # cursor.execute("SELECT COUNT(*) FROM dbo.Fact_Finhub1")
        # result = cursor.fetchone()
        # st.write(f"Number of records in dbo.Fact_Finhub1: {result[0]}")
        # cursor.close()

        # Display basic system metrics
        st.header("System Metrics")
        cpu_usage, memory_usage = get_system_metrics()
        st.write(f"CPU Usage: {cpu_usage}%")
        st.write(f"Memory Usage: {memory_usage}%")

        # Close the database connection
        connection.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    main()
