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
    if os.path.exists('data/data.xlsx'):
        df = pd.read_excel('data/data.xlsx')
    else:
        df = pd.DataFrame()

    # Section to add columns
    st.header("Add Columns to Excel")
    num_cols = st.number_input("Number of Columns to Add", min_value=0, step=1)

    if num_cols > 0:
        new_columns = []
        for i in range(num_cols):
            col_name = st.text_input(f"Enter name for Column {i+1}:", key=f"col_{i}")
            if col_name:
                new_columns.append(col_name)

        if new_columns and st.button("Add Columns"):
            # Add new columns to DataFrame with default value of 0
            for col in new_columns:
                if col not in df.columns:
                    df[col] = 0  # Initialize new columns with 0

            # Save updated DataFrame with new columns to data.xlsx
            df.to_excel('data/data.xlsx', index=False)
            st.write(f"Added {num_cols} new columns to data.xlsx")

    # Section to add rows
    st.header("Add Rows to Excel")
    num_rows = st.number_input("Number of Rows to Add", min_value=0, step=1)

    if num_rows > 0:
        new_data = []
        for i in range(num_rows):
            st.subheader(f"Row {i+1}")
            row_data = {}
            for col in df.columns:
                value = st.text_input(f"Enter value for {col} (Row {i+1}):", key=f"{col}_{i}")
                row_data[col] = value if value else 0  # Set value or keep 0 if input is empty
            new_data.append(row_data)

        if st.button("Add Rows"):
            # Convert new data to DataFrame
            new_df = pd.DataFrame(new_data)

            # Append new data to existing DataFrame
            df = pd.concat([df, new_df], ignore_index=True)

            # Save updated DataFrame to data.xlsx
            df.to_excel('data/data.xlsx', index=False)
            st.write(f"Appended {num_rows} rows of data to data.xlsx")

    # Display the updated DataFrame
    st.header("Updated DataFrame in data.xlsx")
    st.write(df)

if __name__ == "__main__":
    main()
