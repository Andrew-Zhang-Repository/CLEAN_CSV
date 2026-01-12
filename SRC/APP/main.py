import trim
import pandas as pd
import time
import os
import argparse
import mode_utils
import DB
import streamlit as st
from pathlib import Path


st.set_page_config(page_title="CSV Cleaner", layout="wide")

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1px;
        margin-bottom: 1rem;
        height: 5px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>CSV Cleaner</h1>", unsafe_allow_html=True)


OUTPUT_FOLDER = os.path.join("..", "output_CSV")
GLOBAL_REMOVE = ""



with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Log in", type="primary", use_container_width=True):
            st.login()

if st.user.is_logged_in:
    DB.insert_user(st.user.get("email"), st.user.get("email"), "sha256")
    
   
    st.subheader("User Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        history = st.button("Get File History", use_container_width=True)
    
    with col2:
        user_info = st.button("Get User Information", use_container_width=True)

    if history:
        txt = DB.get_user_files(DB.get_user_id(st.user.get("email")))

        if txt != None:
            st.download_button(
                label="Download History as TXT",
                data=txt,
                file_name='history.txt',
                on_click="ignore",
                mime='text/plain',
                use_container_width=True
            )
        else:
            st.markdown("YOU HAVE NEVER PROCESSED A FILE IN THIS SESSION OR EVER")

    if user_info:
        info = DB.get_user_info(st.user.get("email"))
        st.info(f"ID, Email, Date Joined: {info}")
    
    st.markdown("</div>", unsafe_allow_html=True)

if st.user.is_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Log out", use_container_width=True):
            st.logout()


def main():
    
    st.subheader("Upload CSV File")
    
    path = st.file_uploader("Choose a CSV file to clean", type="csv")
    
    st.markdown("</div>", unsafe_allow_html=True)

    if path is not None:


        
        st.subheader("Processing Options")
        
        options = ['Summary', 'Analysis', 'Scan']
        selected_options = st.multiselect(
            "Choose processing modes",
            options,
        )

        clicked = st.button("Run Process", type="primary", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

        df = pd.read_csv(path, low_memory=False)
        df.head()

       

        if clicked:
           

            with st.spinner("Processing your CSV file..."):
                path.seek(0)

                

                
                
                st.subheader("Preview of Original Data")
                st.dataframe(df.head(), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                csv_name = path.name
                bytes_data = path.getvalue()
                file_size_bytes = len(bytes_data)

                header = df.columns
                header_list = header.tolist()
            
                trimmed = trim.clean_up_and_trim(df)
                trimmed.drop_duplicates()
                trimmed.columns = header_list

                for col in trimmed.columns:
                    if trimmed[col].dtype == object:  
                        trimmed[col] = trimmed[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

                curr_time = time.time()
                file_name = "output" + str(curr_time) + ".csv"
                output_file = os.path.join(OUTPUT_FOLDER, file_name)
                trimmed.to_csv(output_file, index=False)

                if st.user.is_logged_in:
                    email = st.user.get("email")
                    user_id = DB.get_user_id(email)
                    DB.insert_file(user_id, csv_name, file_size_bytes, "")

            st.success("Processing complete!")

            ai_text = ""

            if "Summary" in selected_options:
                ai_text += get_ai_modes(None,True,None,df)
            if "Analysis" in selected_options:
                ai_text += get_ai_modes(True,None,None,df)
            if "Scan" in selected_options:
                ai_text += get_ai_modes(None,None,True,df)

            st.markdown(f"AI AGENT OUTPUT: \n\n {ai_text}")
            
            st.subheader("Download Cleaned File")
            
            if os.path.exists(output_file):
                with open(output_file, "rb") as file:
                    btn = st.download_button(
                        label="Download Cleaned CSV",
                        data=file, 
                        file_name=os.path.basename(output_file), 
                        on_click=cleanup_files,
                        args=(OUTPUT_FOLDER,),
                        mime="text/csv",
                        key="download_button_key",
                        use_container_width=True
                    )
            else:
                st.error(f"File not found at path: {output_file}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            


    return None


def get_ai_modes(analysis, summary, scan, path):
    return_str = ""

    if analysis != None:
        return_str += "ANALYSIS: \n\n" + mode_utils.summary("gpt-4o-mini", 0.0, path, "analysis") + "\n\n\n\n"

    if summary != None:
        return_str += "SUMMARY: \n\n" + mode_utils.summary("gpt-4o-mini", 0.0, path, "summary") + "\n\n\n\n"

    if scan != None:
        return_str += "SCAN: \n\n" + mode_utils.summary("gpt-4o-mini", 0.0, path, "scan") + "\n\n\n\n"

    return return_str


def remove_stuff(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        os.remove(file_path)


def cleanup_files(folder_path):
    try:
        
        remove_stuff(folder_path)
      
        
        st.toast("Files cleaned up successfully!")
    except Exception as e:
        st.error(f"Error removing files")


if __name__ == "__main__":
    DB.init_tables()
    main()