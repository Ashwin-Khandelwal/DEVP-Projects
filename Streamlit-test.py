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

# Function to parse the date column automatically
def parse_date_column(data):
    date_column = None
    for column in data.columns:
        try:
            # Attempt to parse the column as datetime
            data[column] = pd.to_datetime(data[column], errors='coerce')
            if pd.api.types.is_datetime64_any_dtype(data[column]):
                date_column = column
                break
        except (ValueError, TypeError):
            continue
    return data, date_column

# Function to visualize time series data
def visualize_time_series(data, date_column):
    st.markdown("### Time Series Analysis")
    
    # Select a numerical column for the y-axis
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    y_column = st.selectbox("Select a numerical column to plot over time", numeric_columns)
    
    if y_column and date_column:
        # Ensure that the data is sorted by the date column
        data = data.sort_values(by=date_column)
        
        st.markdown(f"**Line Chart for {y_column} over {date_column}**")
        
        plt.figure(figsize=(10, 6))
        plt.plot(data[date_column], data[y_column], color='blue')
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
            
            # Automatically detect and parse the date column
            data, date_column = parse_date_column(data)
            
            if date_column:
                # Visualize time series with the detected date column
                visualize_time_series(data, date_column)
            else:
                st.warning("No valid date column found in the dataset.")
        else:
            st.error("Unable to load the data.")
    
if __name__ == '__main__':
    main()
