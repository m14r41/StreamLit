import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

# Function to read and display data from uploaded file
def read_data(file):
    if file is not None:
        file_type = file.name.split('.')[-1]
        if file_type.lower() in ['csv', 'xlsx', 'xls']:
            if file_type.lower() == 'csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, engine='openpyxl')

            st.write("### Data Preview:")
            st.write(df.head())

            return df
        else:
            st.error("Please upload a CSV or Excel file.")

# Function to plot data as bar chart
def plot_bar_chart(df):
    st.write("### Bar Chart:")
    st.write("Select columns to plot:")
    if df is not None:
        # Select columns for plotting
        x_column = st.selectbox("X-axis:", options=df.columns, key='bar_x')
        y_column = st.selectbox("Y-axis:", options=df.columns, index=1, key='bar_y')

        # Plot bar chart using Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x=df[x_column], y=df[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"Bar Chart: {y_column} vs {x_column}")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as line chart
def plot_line_chart(df):
    st.write("### Line Chart:")
    st.write("Select columns to plot:")
    if df is not None:
        # Select columns for plotting
        x_column = st.selectbox("X-axis:", options=df.columns, key='line_x')
        y_column = st.selectbox("Y-axis:", options=df.columns, index=1, key='line_y')

        # Plot line chart using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(df[x_column], df[y_column], marker='o')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"Line Chart: {y_column} vs {x_column}")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as scatter plot
def plot_scatter_plot(df):
    st.write("### Scatter Plot:")
    st.write("Select columns to plot:")
    if df is not None:
        # Select columns for plotting
        x_column = st.selectbox("X-axis:", options=df.columns, key='scatter_x')
        y_column = st.selectbox("Y-axis:", options=df.columns, index=1, key='scatter_y')

        # Plot scatter plot using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.scatter(df[x_column], df[y_column])
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f"Scatter Plot: {y_column} vs {x_column}")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as heatmap
def plot_heatmap(df):
    st.write("### Heatmap:")
    st.write("Select columns for heatmap:")
    if df is not None:
        # Select columns for plotting
        columns = st.multiselect("Select columns:", options=df.columns, key='heatmap')

        # Plot heatmap using Seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(df[columns].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("Heatmap")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as histogram
def plot_histogram(df):
    st.write("### Histogram:")
    st.write("Select a column for histogram:")
    if df is not None:
        # Select column for plotting
        column = st.selectbox("Select a column:", options=df.columns, key='histogram')

        # Plot histogram using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.hist(df[column], bins=20, edgecolor='black')
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.title(f"Histogram: {column}")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as pairplot (for multiple variables)
def plot_pairplot(df):
    st.write("### Pairplot:")
    if df is not None:
        # Plot pairplot using Seaborn
        sns.pairplot(df)
        plt.title("Pairplot")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as pie chart
def plot_pie_chart(df):
    st.write("### Pie Chart:")
    if df is not None:
        # Select column for plotting
        column = st.selectbox("Select a column:", options=df.columns, key='pie_chart')

        # Plot pie chart using Matplotlib
        plt.figure(figsize=(8, 8))
        plt.pie(df[column].value_counts(), labels=df[column].value_counts().index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Pie Chart: {column}")
        st.pyplot()
    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Main function
def main():
    st.title("Data Visualization App")

    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        df = read_data(uploaded_file)

        if df is not None:
            plot_bar_chart(df)
            plot_line_chart(df)
            plot_scatter_plot(df)
            plot_heatmap(df)
            plot_histogram(df)
            plot_pairplot(df)
            plot_pie_chart(df)

if __name__ == "__main__":
    main()
