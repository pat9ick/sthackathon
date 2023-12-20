import streamlit as st
import pyodbc
import psutil
import matplotlib.pyplot as plt
import numpy as np

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

# Function to create a gauge chart
def create_gauge(value, max_value, label):
    angle = value / max_value * 180  # Calculate the angle based on the value

    # Create a gauge plot
    fig, ax = plt.subplots(figsize=(3, 1.5), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)

    # Plot the gauge background
    ax.set_yticklabels([])
    ax.set_ylim(0, 180)
    ax.plot([0, 0], [0, 180], linewidth=2, color='black')

    # Plot the filled portion of the gauge
    ax.fill_between([0, np.radians(angle)], 0, 180, color='green', alpha=0.5)

    # Add a label with the current value
    ax.text(0.5, 0.5, f'{value}/{max_value}\n{label}', transform=ax.transAxes,
            horizontalalignment='center', verticalalignment='center', fontsize=10)

    return fig

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

        # Get system metrics
        cpu_usage, memory_usage = get_system_metrics()

        # Create and display CPU usage gauge
        st.subheader("CPU Usage")
        cpu_gauge_fig = create_gauge(cpu_usage, 100, "Percentage")
        st.pyplot(cpu_gauge_fig)

        # Create and display Memory usage gauge
        st.subheader("Memory Usage")
        memory_gauge_fig = create_gauge(memory_usage, 100, "Percentage")
        st.pyplot(memory_gauge_fig)

        # Display Performance Gauge Chart
        st.subheader("Performance Gauge Chart")
        st.pyplot(plt)

        # Close the database connection
        connection.close()
    else:
        st.error("Failed to connect to the database.")

if __name__ == "__main__":
    main()
