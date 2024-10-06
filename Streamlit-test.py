import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Handle crashing issue by using a more resource-efficient caching mechanism
@st.cache_data
def load_data():
    # Replace with your actual data loading mechanism
    return pd.read_csv('your_data_file.csv')

@st.cache_data
def clean_data(data):
    # Convert categorical variables to numerical where appropriate
    data_cleaned = data.copy()
    
    # Handle categorical variables by converting them to codes or dummy variables
    for col in data_cleaned.columns:
        if data_cleaned[col].dtype == 'object':
            data_cleaned[col] = data_cleaned[col].astype('category').cat.codes
    return data_cleaned

# Additional helper functions to prevent crashes during plotting
@st.cache_resource
def correlation_heatmap(data):
    st.subheader("Correlation Heatmap (Numerical Columns)")
    corr = data.corr(numeric_only=True)  # Ensures only numerical columns are used
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

@st.cache_resource
def distribution_plots(data, numeric_columns):
    st.subheader("Distribution Plots")
    for col in numeric_columns:
        fig, ax = plt.subplots()
        sns.histplot(data[col], kde=True, ax=ax)
        st.pyplot(fig)

def main():
    st.title("Enhanced Data Analysis Dashboard")
    
    # Load data
    data = load_data()
    
    # Cleaning data
    data_cleaned = clean_data(data)
    
    # Sidebar menu
    st.sidebar.header("Options")
    numeric_columns = data_cleaned.select_dtypes(include=[np.number]).columns.tolist()

    st.sidebar.header("Additional Analysis")
    
    # Correlation Heatmap
    if st.sidebar.checkbox("Correlation Heatmap (Numerical)"):
        correlation_heatmap(data_cleaned)
    
    # Distribution plots
    if st.sidebar.checkbox("Distribution Plots (Numerical)"):
        distribution_plots(data_cleaned, numeric_columns)

if __name__ == "__main__":
    main()
