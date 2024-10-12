# Import necessary libraries for Streamlit, Data Analysis, and Visualization
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for plots
sns.set(style="whitegrid")

# Page Config
st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

# Function to upload and load dataset
def load_data():
    with st.sidebar:
        st.header("Upload Dataset")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("Data successfully loaded!")
        return data
    else:
        st.warning("Please upload a CSV file.")
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

# Function to analyze and visualize a selected categorical column
def visualize_categorical_column(data):
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
    if len(categorical_columns) > 0:
        st.markdown("### Categorical Data Visualization")
        column_name = st.selectbox("Select a categorical column", categorical_columns)
        
        if column_name:
            st.markdown(f"**Bar Chart for {column_name}**")
            category_counts = data[column_name].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Category', y='Count', data=category_counts)
            st.pyplot(plt)

# Main App Function
def main():
    st.title("Data Analysis Dashboard")
    
    data = load_data()
    
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
