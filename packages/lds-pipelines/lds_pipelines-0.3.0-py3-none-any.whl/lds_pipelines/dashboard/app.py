
import streamlit as st
import subprocess
import sys
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


from lds_pipelines.dashboard.intro_page import show_intro_page  
from lds_pipelines.dashboard.csv_page import show_csv_page
from lds_pipelines.dashboard.api_page import show_api_page


def main():
    st.sidebar.title("Leak Detection System")
    
    pages = {
        "Introduction": show_intro_page,
        "Static Analysis": show_csv_page,
        "Real-time Analysis": show_api_page
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    pages[selection]()

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="footer">LDS- \n Developed by Aman Sharma<br>© 2025</div>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

def run():
    subprocess.run(["streamlit", "run", os.path.abspath(__file__)])
   

if __name__ == "__main__":
    st.set_page_config(
    page_title="Leak Detection Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        .footer {
            font-size: 0.9rem;
            color: gray;
            margin-top: 200;
        }
        </style>
    """, unsafe_allow_html=True)
    
    main()