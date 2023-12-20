import streamlit as st
import pyodbc
import psutil

# Function to connect to the database
def db_connect():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
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

# Function to create a performance gauge chart
def performance_gauge_chart(percentage):
    # Display a progress bar to represent the performance
    st.subheader("Performance Gauge Chart")
    st.progress(percentage / 100)

    # Display the percentage value
    st.write(f"Performance: {percentage}%")

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
        # st.write(f"Number of records in dbo.Fact_Finhub1: {result[0]}
