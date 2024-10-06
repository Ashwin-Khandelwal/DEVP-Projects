# Import necessary libraries for Streamlit, Data Analysis, and Visualization
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for plots
sns.set(style="whitegrid")

# Sample dataset to test if app works
sample_data = pd.DataFrame({
    'Category': ['A', 'B', 'A', 'C', 'B', 'A'],
    'Values': [10, 20, 15, 25, 10, 30]
})

# Function to show basic data information
def show_data_overview(data):
    st.subheader("Data Overview")
    st.write("Dataset Preview:")
    st.dataframe(data.head())
    
    st.write("Basic Statistics:")
    st.write(data.describe())

# Function to analyze and visualize a selected numerical column
def visualize_numeric_column(data):
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_columns) > 0:
        st.subheader("Numerical Data Visualization")
        column_name = st.selectbox("Select a numerical column", numeric_columns)
        
        if column_name:
            st.write(f"Histogram for {column_name}")
            fig, ax = plt.subplots()
            sns.histplot(data[column_name], kde=True, ax=ax)
            st.pyplot(fig)
    else:
        st.warning("No numerical columns found for visualization.")

# Main function to render the Streamlit app
def main():
    st.title("Basic Data Analysis Dashboard")
    
    # Load the sample data instead of uploading a CSV
    data = sample_data
    show_data_overview(data)
    visualize_numeric_column(data)

if __name__ == "__main__":
    main()
