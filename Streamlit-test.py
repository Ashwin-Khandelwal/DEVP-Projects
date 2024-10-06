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
    
    with st.beta_expander("View Dataset Statistics"):
        st.write(data.describe())

# Function to analyze and visualize a selected numerical column
def visualize_numeric_column(data):
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_columns) > 0:
        st.markdown("### Numerical Data Visualization")
        column_name = st.selectbox("Select a numerical column", numeric_columns)
        
        if column_name:
            st.markdown(f"**Histogram for {column_name}**")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data[column_name], kde=True, ax=ax, color="skyblue")
            ax.set_title(f'Distribution of {column_name}', fontsize=14)
            ax.set_xlabel(column_name)
            ax.set_ylabel('Frequency')
            st.pyplot(fig)
    else:
        st.warning("No numerical columns found for visualization.")

# Function to analyze and visualize a selected categorical column
def analyze_categorical_column(data):
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    if len(categorical_columns) > 0:
        st.markdown("### Categorical Data Visualization")
        column_name = st.selectbox("Select a categorical column", categorical_columns)
        
        if column_name:
            st.markdown(f"**Bar Chart for {column_name}**")
            freq = data[column_name].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(y=data[column_name], order=freq.index, ax=ax, palette="Set2")
            ax.set_title(f'Distribution of {column_name}', fontsize=14)
            ax.set_xlabel('Count')
            ax.set_ylabel(column_name)
            st.pyplot(fig)
    else:
        st.warning("No categorical columns found for visualization.")

# Main function to render the Streamlit app
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Visualizations"])

    # Load the data through file uploader
    data = load_data()

    if data is not None:
        if page == "Overview":
            st.title("📊 Data Overview")
            show_data_overview(data)
        elif page == "Visualizations":
            st.title("📈 Data Visualizations")
            st.sidebar.header("Visualization Options")
            st.sidebar.markdown("Select columns to visualize.")
            
            # Allow user to toggle between numeric and categorical visualizations
            visualize_type = st.sidebar.radio("Choose data type", ["Numerical", "Categorical"])
            
            if visualize_type == "Numerical":
                visualize_numeric_column(data)
            elif visualize_type == "Categorical":
                analyze_categorical_column(data)
    else:
        st.markdown("### Upload a CSV file to start exploring the data.")

if __name__ == "__main__":
    main()
