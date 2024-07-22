import streamlit as st
import pandas as pd
import os
import copy

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

    # To keep the previous state of the DataFrame for undo functionality
    if 'prev_df' not in st.session_state:
        st.session_state.prev_df = None

    def save_previous_state():
        st.session_state.prev_df = copy.deepcopy(df)

    # Section to add columns
    st.header("Add Columns to Excel")
    num_cols = st.number_input("Number of Columns to Add", min_value=0, step=1, key="num_cols")

    if num_cols > 0:
        with st.form(key='add_columns_form'):
            new_columns = []
            for i in range(num_cols):
                col_name = st.text_input(f"Enter name for Column {i+1}:", key=f"col_{i}")
                if col_name:
                    new_columns.append(col_name)
            if st.form_submit_button("Add Columns"):
                save_previous_state()
                # Add new columns to DataFrame with default value of 0
                for col in new_columns:
                    if col not in df.columns:
                        df[col] = 0  # Initialize new columns with 0

                # Save updated DataFrame with new columns to data.xlsx
                df.to_excel('data/data.xlsx', index=False)
                st.write(f"Added {num_cols} new columns to data.xlsx")
                st.experimental_rerun()  # Clear the inputs by rerunning the script

    # Section to add rows
    st.header("Add Rows to Excel")
    num_rows = st.number_input("Number of Rows to Add", min_value=0, step=1, key="num_rows")

    if num_rows > 0:
        with st.form(key='add_rows_form'):
            new_data = []
            for i in range(num_rows):
                st.subheader(f"Row {i+1}")
                row_data = {}
                for col in df.columns:
                    value = st.text_input(f"Enter value for {col} (Row {i+1}):", key=f"{col}_{i}")
                    row_data[col] = value if value else 0  # Set value or keep 0 if input is empty
                new_data.append(row_data)

            if st.form_submit_button("Add Rows"):
                save_previous_state()
                # Convert new data to DataFrame
                new_df = pd.DataFrame(new_data)

                # Append new data to existing DataFrame
                df = pd.concat([df, new_df], ignore_index=True)

                # Save updated DataFrame to data.xlsx
                df.to_excel('data/data.xlsx', index=False)
                st.write(f"Appended {num_rows} rows of data to data.xlsx")
                st.experimental_rerun()  # Clear the inputs by rerunning the script

    # Section to clear the table
    if st.button("Clear Table"):
        save_previous_state()
        df = pd.DataFrame()  # Reset DataFrame
        df.to_excel('data/data.xlsx', index=False)
        st.write("Cleared all data and reset the table.")
        st.experimental_rerun()  # Clear the inputs by rerunning the script

    # Section to undo the last change
    if st.button("Undo") and st.session_state.prev_df is not None:
        df = st.session_state.prev_df
        df.to_excel('data/data.xlsx', index=False)
        st.write("Reverted to the previous state of the table.")
        st.session_state.prev_df = None  # Clear the previous state after undo
        st.experimental_rerun()  # Clear the inputs by rerunning the script

    # Display the updated DataFrame
    st.header("Updated DataFrame in data.xlsx")
    st.write(df)

if __name__ == "__main__":
    main()
