# Importing necessary libraries for Streamlit, Data Analysis, and Visualization
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import chi2_contingency

# Set the style for plots
sns.set(style="whitegrid")

# Function to upload and load dataset
def load_data():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("Data successfully loaded!")
        return data
    else:
        st.warning("Please upload a CSV file.")
        return None

# Function to analyze and visualize categorical columns
def analyze_categorical_column(data, column_name):
    st.subheader(f"Analysis for {column_name}")
    freq = data[column_name].value_counts()
    proportion = data[column_name].value_counts(normalize=True) * 100

    st.write("Value Counts:")
    st.dataframe(freq)
    st.write("Proportion (%):")
    st.dataframe(proportion)

    # Plotting bar chart for categorical data
    if len(freq) > 10:
        st.write(f"Top 10 Categories of {column_name}:")
        top_10 = freq.head(10)
        others = freq[10:].sum()
        pie_labels = top_10.index.tolist() + ['Other']
        pie_values = top_10.tolist() + [others]

        # Create labels with percentages for the legend
        pie_percentages = [(value / freq.sum()) * 100 for value in pie_values]
        legend_labels = [f"{label}: {value:.1f}%" for label, value in zip(pie_labels, pie_percentages)]

        # Plot pie chart with explode
        explode = [0.05] * len(pie_values)  # Small separation for each slice
        colors = sns.color_palette('Set3', len(pie_values) - 1) + ['#808080']

        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, _ = ax.pie(pie_values, explode=explode, colors=colors, startangle=140)
        ax.legend(wedges, legend_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.set_title(f"Top 10 Distribution of {column_name} (Others grouped)")
        st.pyplot(fig)
    else:
        st.write(f"Pie Chart of {column_name}:")
        fig, ax = plt.subplots(figsize=(10, 6))
        freq.plot.pie(autopct='%1.1f%%', colors=sns.color_palette('viridis', len(freq)), ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)

# Function to calculate Cramér's V (correlation for categorical variables)
def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    return np.sqrt(chi2 / (n * (min(confusion_matrix.shape) - 1)))

# Function to calculate and display correlation between categorical columns
def calculate_correlation(df, column, categorical_columns):
    st.subheader(f"Correlation Analysis for {column}")
    for other_col in categorical_columns:
        if other_col != column:
            confusion_matrix = pd.crosstab(df[column], df[other_col])
            if confusion_matrix.shape[0] > 1 and confusion_matrix.shape[1] > 1:
                corr = cramers_v(confusion_matrix)
                st.write(f"Cramér's V Correlation between '{column}' and '{other_col}': {corr:.4f}")
            else:
                st.write(f"Skipping correlation calculation for '{column}' and '{other_col}' (only one category).")

# Main function to render the Streamlit app
def main():
    st.title("Categorical Data Analysis Dashboard")
    
    data = load_data()
    
    if data is not None:
        categorical_columns = ['Payment_Terms', 'Country', 'Product', 'Import_Export', 'Category', 'Customs_Code', 'Shipping_Method', 'Supplier', 'Customer']
        
        column_name = st.selectbox("Select a categorical column to analyze", categorical_columns)
        
        if column_name:
            analyze_categorical_column(data, column_name)
            calculate_correlation(data, column_name, categorical_columns)

if __name__ == "__main__":
    main()
