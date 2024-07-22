import streamlit as st
import subprocess

def run_script(script_name):
    # Specify full path to scripts if they are not in the same directory
    script_paths = {
        'tables': 'tables.py',
        'main': 'main.py',
        'app': 'app.py',
        'tables2': 'deltable.py',
        'graph': 'graph.py',
    }
    
    if script_name in script_paths:
        command = ['streamlit', 'run', script_paths[script_name]]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            st.error(f"Error occurred: {stderr.decode('utf-8')}")
        else:
            st.success(f"Successfully ran script: {script_name}")
    else:
        st.error(f"Script '{script_name}' not found.")

def main():
    st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

    # Custom CSS to position the sidebar at the top
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            padding-top: 0px;
        }
        .block-container {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Streamlit Dashboard Menu")

    st.sidebar.title("Select Script to Run")
    script_to_run = st.sidebar.selectbox("Select Application", ["tables", "main", "app", "tables2","graph"])

    if st.sidebar.button("Run Page"):
        run_script(script_to_run)

if __name__ == "__main__":
    main()
