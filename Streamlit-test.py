# Import necessary libraries for Streamlit, Data Analysis, and Visualization
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
def reduce_cardinality_in_column(column_data, threshold=10):
    value_counts = column_data.value_counts()
    
    # Only reduce cardinality if the column has more unique values than the threshold
    if len(value_counts) > threshold:
        mask = column_data.isin(value_counts.index[threshold:])
        column_data[mask] = 'Other'
    
    return column_data

# Function to analyze and visualize a selected categorical column with sampling
def visualize_categorical_column(data):
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(categorical_columns) > 0:
        st.markdown("### Categorical Data Visualization")
        column_name = st.selectbox("Select a categorical column", categorical_columns)
        
        if column_name:
            column_data = data[column_name].copy()
            
            # Sample large columns for better performance
            if len(column_data) > 5000:
                column_data = column_data.sample(5000, random_state=1)
                st.info("Sampled 5000 rows for faster processing.")
            
            # Apply cardinality reduction only if necessary
            column_data = reduce_cardinality_in_column(column_data)
            
            st.markdown(f"**Bar Chart for {column_name}**")
            category_counts = column_data.value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Category', y='Count', data=category_counts)
            st.pyplot(plt)

# Main App Function
def main():
    st.title("Data Analysis Dashboard")
    
    # File uploader (must be outside cached functions)
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load data and cache it (only after file is uploaded)
        data = load_data(uploaded_file)
        
        if data is not None:
            # Display data overview
            show_data_overview(data)
            
            # Visualization options
            st.sidebar.header("Visualization Options")
            analysis_type = st.sidebar.radio("Choose analysis type", ('Numerical', 'Categorical'))
            
            if analysis_type == 'Numerical':
                visualize_numeric_column(data)
            elif analysis_type == 'Categorical':
                visualize_categorical_column(data)

if __name__ == '__main__':
    main()
