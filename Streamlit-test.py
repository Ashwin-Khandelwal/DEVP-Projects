# Import necessary libraries for Streamlit, Data Analysis, and Visualization
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for plots
sns.set(style="whitegrid")

# Page Config
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# Function to load data from the uploaded file (cached)
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        # If the dataset is too large, sample a subset to prevent memory issues
        if len(data) > 10000:
            data = data.sample(10000, random_state=1)
            st.warning("The dataset has been sampled to 10,000 rows for better performance.")
        return data
    return None

# Function to show basic data information
def show_data_overview(data):
    st.markdown("### Data Overview")
    st.write("Below is a preview of the dataset and some basic statistics.")
    st.dataframe(data.head(), height=200)
    
    with st.expander("View Dataset Statistics"):
        st.write(data.describe())

# Function to parse the date column
def parse_date_column(data, date_column):
    try:
        data[date_column] = pd.to_datetime(data[date_column])
    except (ValueError, TypeError):
        st.error(f"Failed to parse {date_column} as a date.")
    return data

# Function to filter data by date range
def filter_by_date(data, date_column):
    st.sidebar.subheader("Date Range Filter")
    min_date = data[date_column].min()
    max_date = data[date_column].max()
    date_range = st.sidebar.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = data[(data[date_column] >= pd.to_datetime(start_date)) & (data[date_column] <= pd.to_datetime(end_date))]
        return filtered_data
    return data

# Function to visualize time series data
def visualize_time_series(data, date_column):
    st.markdown("### Time Series Analysis")
    
    # Filter by date range
    filtered_data = filter_by_date(data, date_column)
    
    # Select a numerical column for the y-axis
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    y_column = st.selectbox("Select a numerical column to plot over time", numeric_columns)
    
    if y_column:
        st.markdown(f"**Line Chart for {y_column} over {date_column}**")
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data[date_column], filtered_data[y_column], color='blue')
        plt.xlabel(f"{date_column}")
        plt.ylabel(f"{y_column}")
        plt.title(f"{y_column} over Time")
        plt.xticks(rotation=45)
        st.pyplot(plt)

# Main App Function
def main():
    st.title("Data Analysis Dashboard")
    
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        
        if data is not None:
            # Display data overview
            show_data_overview(data)
            
            # Select the date column for time series analysis
            date_column = st.sidebar.selectbox("Select the date column", data.select_dtypes(include=['object']).columns.tolist())
            
            if date_column:
                # Parse the date column
                data = parse_date_column(data, date_column)
                
                # Visualize time series
                visualize_time_series(data, date_column)

if __name__ == '__main__':
    main()

