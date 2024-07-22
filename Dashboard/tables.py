import streamlit as st
import pandas as pd
import os
import copy
import matplotlib.pyplot as plt

# Function to create directory and Excel file if they do not exist
def create_directory_and_file():
    if not os.path.exists('data'):
        os.makedirs('data')
        st.write("Created directory: data")

    if not os.path.exists('data/data.xlsx'):
        df = pd.DataFrame()
        df.to_excel('data/data.xlsx', index=False)
        st.write("Created new Excel file: data.xlsx")

def load_data():
    # Load existing data from data.xlsx or initialize an empty DataFrame
    if os.path.exists('data/data.xlsx'):
        return pd.read_excel('data/data.xlsx')
    else:
        return pd.DataFrame()

def main():
    st.title("Dynamic Data Entry to Excel")

    # Create directory and file if they do not exist
    create_directory_and_file()

    # Load existing data from data.xlsx or initialize an empty DataFrame
    df = load_data()

    # To keep the previous state of the DataFrame for undo functionality
    if 'prev_df' not in st.session_state:
        st.session_state.prev_df = None

    def save_previous_state():
        st.session_state.prev_df = copy.deepcopy(df)

    # Section to add columns
    st.markdown("""
        <style>
        .header { 
            background-color: #f4a261; 
            padding: 10px; 
            border-radius: 5px; 
            color: #fff; 
            font-size: 20px;
            text-align: center;
        }
        .button { 
            background-color: #2a9d8f; 
            color: white; 
            padding: 10px 20px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer; 
            font-size: 16px;
        }
        .button:hover { 
            background-color: #264653; 
        }
        .section { 
            background-color: #e9c46a; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="header">Add Columns to Excel</div>', unsafe_allow_html=True)

    if 'add_columns_submitted' not in st.session_state:
        st.session_state.add_columns_submitted = False

    num_cols = st.number_input("Number of Columns to Add", min_value=0, step=1, key="num_cols")

    if num_cols > 0:
        with st.form(key='add_columns_form'):
            new_columns = []
            for i in range(num_cols):
                col_name = st.text_input(f"Enter name for Column {i+1}:", key=f"col_{i}")
                if col_name:
                    new_columns.append(col_name)
            submit_button = st.form_submit_button("Add Columns", use_container_width=True)

            if submit_button:
                st.session_state.add_columns_submitted = True
                save_previous_state()
                # Add new columns to DataFrame with default value of 0
                for col in new_columns:
                    if col not in df.columns:
                        df[col] = 0  # Initialize new columns with 0

                # Save updated DataFrame with new columns to data.xlsx
                df.to_excel('data/data.xlsx', index=False)
                st.write(f"Added {num_cols} new columns to data.xlsx")
                
                # Reload the data to ensure the DataFrame reflects the latest state
                df = load_data()
                st.experimental_rerun()
            else:
                st.session_state.add_columns_submitted = False

    # Section to add rows
    st.markdown('<div class="header">Add Rows to Excel</div>', unsafe_allow_html=True)
    
    if 'add_rows_submitted' not in st.session_state:
        st.session_state.add_rows_submitted = False

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

            submit_button = st.form_submit_button("Add Rows", use_container_width=True)

            if submit_button:
                st.session_state.add_rows_submitted = True
                save_previous_state()
                # Convert new data to DataFrame
                new_df = pd.DataFrame(new_data)

                # Append new data to existing DataFrame
                df = pd.concat([df, new_df], ignore_index=True)

                # Save updated DataFrame to data.xlsx
                df.to_excel('data/data.xlsx', index=False)
                st.write(f"Appended {num_rows} rows of data to data.xlsx")
                
                # Reload the data to ensure the DataFrame reflects the latest state
                df = load_data()
                st.experimental_rerun()
            else:
                st.session_state.add_rows_submitted = False

    # Section to clear the table
    if st.button("Clear Table", key="clear_table", help="Clear all data and reset the table", use_container_width=True):
        save_previous_state()
        df = pd.DataFrame()  # Reset DataFrame
        df.to_excel('data/data.xlsx', index=False)
        st.write("Cleared all data and reset the table.")
        st.experimental_rerun()

    # Section to undo the last change
    if st.button("Undo", key="undo", help="Undo the last change", use_container_width=True):
        if st.session_state.prev_df is not None:
            df = st.session_state.prev_df
            df.to_excel('data/data.xlsx', index=False)
            st.write("Reverted to the previous state of the table.")
            st.session_state.prev_df = None  # Clear the previous state after undo
            st.experimental_rerun()

    # Display the DataFrame with editable fields
    st.markdown('<div class="header">Editable DataFrame</div>', unsafe_allow_html=True)
    
    # Display editable DataFrame
    edited_df = st.data_editor(df, use_container_width=True, key='data_editor')

    # Save button
    if st.button("Save", key="save_data", help="Save changes to data.xlsx"):
        edited_df.to_excel('data/data.xlsx', index=False)
        st.write("Changes have been saved to data.xlsx")

    # Reload the data after saving
    df = load_data()

    # Graph view
    st.markdown('<div class="header">Graph View</div>', unsafe_allow_html=True)

    chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Pie Chart"], key="chart_type")

    if not df.empty:
        if chart_type == "Line Chart":
            st.line_chart(df)
        elif chart_type == "Bar Chart":
            st.bar_chart(df)
        elif chart_type == "Pie Chart":
            pie_columns = st.multiselect("Select Columns for Pie Chart", df.columns, key="pie_columns")
            if pie_columns:
                try:
                    pie_data = df[pie_columns].apply(pd.to_numeric, errors='coerce').sum()  # Convert and aggregate the selected columns
                    pie_data = pie_data.dropna()  # Remove NaN values
                    if not pie_data.empty:
                        fig, ax = plt.subplots()
                        ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                        st.pyplot(fig)
                    else:
                        st.write("Selected columns have no valid numeric data for pie chart.")
                except Exception as e:
                    st.error(f"Error generating pie chart: {e}")
    else:
        st.write("No data available for visualization.")

if __name__ == "__main__":
    main()
