import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        # Convert df.columns to list to avoid the ValueError
        columns = list(df.columns)

        # Select columns for plotting
        x_columns = st.multiselect("X-axis:", options=columns, default=[columns[0]], key='bar_x_axis')
        y_columns = st.multiselect("Y-axis:", options=columns, default=[columns[1]], key='bar_y_axis')

        # Filter data based on selected columns
        filter_column = st.selectbox("Filter by:", options=columns, key='bar_filter')
        filter_values = st.multiselect(f"Select {filter_column}:", options=df[filter_column].unique(), key='bar_filter_values')

        if not filter_values:  # If no filter values selected, use entire dataframe
            filtered_df = df
        else:
            filtered_df = df[df[filter_column].isin(filter_values)]

        # Plot bar chart using Seaborn if at least one x_columns and one y_columns is selected
        if x_columns and y_columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            for y_col in y_columns:
                sns.barplot(x=x_columns[0], y=filtered_df[y_col], data=filtered_df, ax=ax, label=y_col)
            ax.set_xlabel(", ".join(x_columns))
            ax.set_ylabel(", ".join(y_columns))
            if filter_values:
                ax.set_title(f"Bar Chart: {', '.join(y_columns)} vs {', '.join(x_columns)} (Filtered by {filter_column}={', '.join(filter_values)})")
            else:
                ax.set_title(f"Bar Chart: {', '.join(y_columns)} vs {', '.join(x_columns)} (Entire Dataset)")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("Please select at least one X-axis and one Y-axis column to plot.")

    else:
        st.warning("Please upload a valid CSV or Excel file to plot charts.")

# Function to plot data as pie chart
def plot_pie_chart(df):
    st.write("### Pie Chart:")
    if df is not None:
        # Convert df.columns to list to avoid the ValueError
        columns = list(df.columns)

        # Select column for plotting
        column = st.selectbox("Select a column:", options=columns, key='pie_chart')

        # Filter data based on selected column
        filter_values = st.multiselect(f"Select {column}:", options=df[column].unique(), key='pie_chart_filter_values')

        if not filter_values:  # If no filter values selected, use entire dataframe
            filtered_df = df
        else:
            filtered_df = df[df[column].isin(filter_values)]

        # Plot pie chart using Matplotlib
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(filtered_df[column].value_counts(), labels=filtered_df[column].value_counts().index, autopct='%1.1f%%', startangle=140)
        ax.set_title(f"Pie Chart: {column} (Filtered by {column}={', '.join(filter_values)})")
        st.pyplot(fig)
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
            plot_pie_chart(df)

if __name__ == "__main__":
    main()
