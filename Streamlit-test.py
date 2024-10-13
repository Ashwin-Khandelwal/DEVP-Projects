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
        return data
    return None

# Function to show basic data information
def show_data_overview(data):
    st.markdown("### Data Overview")
    st.write("Below is a preview of the dataset and some basic statistics.")
    st.dataframe(data.head(), height=200)
    
    with st.expander("View Dataset Statistics"):
        st.write(data.describe())

# Function to filter data based on user input
def filter_data(data):
    st.sidebar.header("Filter Data")
    
    # Filter by categorical variables
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    for column in categorical_columns:
        unique_values = data[column].value_counts()
        
        # Retain all unique values if less than or equal to 6 unique values
        if len(unique_values) <= 6:
            top_values = unique_values.index.tolist()  # Show all values
        else:
            # Limit to top 5 or 6 categories by frequency
            top_values = unique_values.head(6).index.tolist()
        
        # Initialize with all values selected, but don't enable the filter by default
        selected_values = st.sidebar.multiselect(f"Select {column} (optional)", top_values, default=None)
        
        # Only apply filter if some values are selected
        if selected_values:
            data = data[data[column].isin(selected_values)]
    
    # Filter by numerical variables
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    for column in numerical_columns:
        min_val = float(data[column].min())
        max_val = float(data[column].max())
        # Limit range to avoid excessive slider lengths
        capped_min = max(min_val, -1e6)
        capped_max = min(max_val, 1e6)
        selected_range = st.sidebar.slider(f"Select range for {column} (optional)", capped_min, capped_max, (capped_min, capped_max))
        
        # Only apply filter if a valid range is selected
        if not np.isnan(selected_range[0]) and not np.isnan(selected_range[1]):
            data = data[(data[column] >= selected_range[0]) & (data[column] <= selected_range[1])]
    
    return data

# Function to analyze and visualize a selected numerical column
def visualize_numeric_column(data):
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_columns) > 0:
        st.markdown("### Numerical Data Visualization")
        column_name = st.selectbox("Select a numerical column", numeric_columns)
        
        if column_name:
            st.markdown(f"**Histogram for {column_name}**")
            plt.figure(figsize=(10, 6))
            plt.hist(data[column_name], bins=30, color='skyblue', edgecolor='black')
            st.pyplot(plt)

# Function to reduce cardinality in a specific categorical column
def reduce_cardinality_in_column(column_data, max_categories=10):
    value_counts = column_data.value_counts()
    
    if len(value_counts) > max_categories:
        top_categories = value_counts.index[:max_categories]
        mask = ~column_data.isin(top_categories)
        column_data[mask] = 'Other'
    
    return column_data

# Function to analyze and visualize a selected categorical column with sampling and limiting categories
def visualize_categorical_column(data):
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(categorical_columns) > 0:
        st.markdown("### Categorical Data Visualization")
        column_name = st.selectbox("Select a categorical column", categorical_columns)
        
        if column_name:
            column_data = data[column_name].copy()
            
            if len(column_data) > 5000:
                column_data = column_data.sample(5000, random_state=1)
                st.info("Sampled 5000 rows for faster processing.")
            
            column_data = reduce_cardinality_in_column(column_data)
            
            st.markdown(f"**Bar Chart for {column_name}**")
            category_counts = column_data.value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Category', y='Count', data=category_counts)
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
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
            
            # Filter the data based on user input
            filtered_data = filter_data(data)
            
            # Visualization options
            st.sidebar.header("Visualization Options")
            analysis_type = st.sidebar.radio("Choose analysis type", ('Numerical', 'Categorical'))
            
            if analysis_type == 'Numerical':
                visualize_numeric_column(filtered_data)
            elif analysis_type == 'Categorical':
                visualize_categorical_column(filtered_data)

if __name__ == '__main__':
    main()
