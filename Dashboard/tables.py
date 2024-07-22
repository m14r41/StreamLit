import streamlit as st
import pandas as pd
import os

# Function to create directory and Excel file if they do not exist
def create_directory_and_file():
    if not os.path.exists('data'):
        os.makedirs('data')
        st.write("Created directory: data")

    if not os.path.exists('data/data.xlsx'):
        df = pd.DataFrame()
        df.to_excel('data/data.xlsx', index=False)
        st.write("Created new Excel file: data.xlsx")

def main():
    st.title("Dynamic Data Entry to Excel")

    # Create directory and file if they do not exist
    create_directory_and_file()

    # Load existing data from data.xlsx or initialize an empty DataFrame
    df = pd.read_excel('data/data.xlsx') if os.path.exists('data/data.xlsx') else pd.DataFrame()

    # Allow user to input columns
    st.header("Add Columns to Excel")
    num_cols = st.number_input("Number of Columns to Add", min_value=0, step=1)

    if num_cols > 0:
        new_columns = []
        for i in range(num_cols):
            col_name = st.text_input(f"Enter name for Column {i+1}:")
            if col_name:
                new_columns.append(col_name)

        if new_columns:
            # Add new columns to DataFrame
            for col in new_columns:
                df[col] = None  # Initialize new columns with None values

            # Save updated DataFrame with new columns to data.xlsx
            df.to_excel('data/data.xlsx', index=False)
            st.write(f"Added {num_cols} new columns to data.xlsx")

    # Display section for adding rows
    st.header("Add Rows to Excel")

    # Input for number of rows
    num_rows = st.number_input("Number of Rows to Add", min_value=1, step=1)

    if num_rows > 0:
        new_data = []
        for i in range(num_rows):
            row_data = {}
            for col in df.columns:
                value = st.text_input(f"Enter value for {col} (Row {i+1}):", key=f"{col}_{i}")
                row_data[col] = value
            new_data.append(row_data)
        
        # Convert new data to DataFrame
        new_df = pd.DataFrame(new_data)

        # Append new data to existing DataFrame if it exists, otherwise use new_df
        if df.empty:
            df = new_df
        else:
            df = pd.concat([df, new_df], ignore_index=True)

        # Save updated DataFrame to data.xlsx
        df.to_excel('data/data.xlsx', index=False)
        st.write(f"Appended {num_rows} rows of data to data.xlsx")

    # Display the updated DataFrame
    st.header("Updated DataFrame in data.xlsx")
    st.write(df)

if __name__ == "__main__":
    main()
