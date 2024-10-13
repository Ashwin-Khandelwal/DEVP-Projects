import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set plot styles
sns.set(style="whitegrid")

# Page Config
st.set_page_config(page_title="Data Visualization and Descriptive Statistics", layout="wide")

# Function to load data from the uploaded file (cached for performance)
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        if len(data) > 10000:
            data = data.sample(10000, random_state=1)  # Sample large datasets for performance
            st.warning("The dataset has been sampled to 10,000 rows for better performance.")
        return data
    return None

# Function to show descriptive statistics for numerical variables
def show_numerical_stats(data):
    st.markdown("### Descriptive Statistics for Numerical Variables")
    numerical_data = data.select_dtypes(include=['float64', 'int64'])
    
    if not numerical_data.empty:
        st.write(numerical_data.describe())
    else:
        st.warning("No numerical columns found.")

# Function to show frequency counts for categorical variables
def show_categorical_stats(data):
    st.markdown("### Descriptive Statistics for Categorical Variables")
    categorical_data = data.select_dtypes(include=['object', 'category'])
    
    if not categorical_data.empty:
        for column in categorical_data.columns:
            st.markdown(f"**{column}**")
            st.write(categorical_data[column].value_counts())
    else:
        st.warning("No categorical columns found.")

# Function to visualize numerical variables (histogram)
def visualize_numerical(data):
    st.markdown("### Numerical Variable Visualization")
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if numerical_columns:
        selected_column = st.selectbox("Select a numerical column", numerical_columns)
        if selected_column:
            plt.figure(figsize=(10, 6))
            sns.histplot(data[selected_column], kde=True)
            plt.title(f"Distribution of {selected_column}")
            plt.xlabel(selected_column)
            plt.ylabel("Frequency")
            st.pyplot(plt)
    else:
        st.warning("No numerical columns available for visualization.")

# Function to visualize categorical variables (bar chart)
def visualize_categorical(data):
    st.markdown("### Categorical Variable Visualization")
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()

    if categorical_columns:
        selected_column = st.selectbox("Select a categorical column", categorical_columns)
        if selected_column:
            plt.figure(figsize=(10, 6))
            sns.countplot(y=data[selected_column], palette="viridis")
            plt.title(f"Count of Categories in {selected_column}")
            plt.ylabel(selected_column)
            plt.xlabel("Count")
            st.pyplot(plt)
    else:
        st.warning("No categorical columns available for visualization.")

# Main app function
def main():
    st.title("Data Visualization and Descriptive Statistics Dashboard")

    # Upload the CSV file
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Load the data
        data = load_data(uploaded_file)

        if data is not None:
            # Show the first few rows of the data
            st.markdown("### Dataset Preview")
            st.dataframe(data.head(), height=200)

            # Show descriptive statistics for numerical variables
            show_numerical_stats(data)

            # Show frequency counts for categorical variables
            show_categorical_stats(data)

            # Allow the user to visualize either numerical or categorical variables
            st.markdown("## Visualizations")
            visualization_type = st.selectbox("Choose the type of visualization", ["Numerical", "Categorical"])

            if visualization_type == "Numerical":
                visualize_numerical(data)
            else:
                visualize_categorical(data)
        else:
            st.error("Unable to load data. Please check the file format.")
    else:
        st.info("Please upload a CSV file to get started.")

# Run the app
if __name__ == '__main__':
    main()
