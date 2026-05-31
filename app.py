import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Sales Recon", layout="centered")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    /* Button ko center karne ke liye */
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        width: 100%;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        margin-top: 20px;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
    }
    /* Title ko center aur style karne ke liye */
    h1 {
        text-align: center;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

PASSWORD = "Raman@2026"

def main():
    st.title("📊 Sales Reconciliation")
    st.markdown("---")
    
    user_pass = st.text_input("Enter Password:", type="password")
    
    if user_pass == PASSWORD:
        col1, col2 = st.columns(2)
        with col1:
            tally_file = st.file_uploader("Tally Excel", type=['xlsx'])
        with col2:
            portal_file = st.file_uploader("Portal Excel", type=['xlsx'])
        
        if tally_file and portal_file:
            # Button ab center mein aur bada dikhega
            if st.button("🚀 Reconcile Data Now"):
                with st.spinner('Data process ho raha hai...'):
                    df_tally = pd.read_excel(tally_file, header=1)
                    df_portal = pd.read_excel(portal_file)
                    
                    df_tally.columns = ['Date', 'Party Name', 'Amount']
                    df_portal.columns = ['Date', 'Party Name', 'Amount']
                    
                    df_tally['Date'] = pd.to_datetime(df_tally['Date']).dt.strftime('%d-%m-%Y')
                    df_portal['Date'] = pd.to_datetime(df_portal['Date']).dt.strftime('%d-%m-%Y')
                    
                    merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                    merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                    
                    st.success("Reconciliation Complete!")
                    st.dataframe(merged_df, use_container_width=True)
                    
                    # Download Section
                    output = io.BytesIO()
                    merged_df.to_excel(output, index=False)
                    st.download_button("📥 Download Final Report", output.getvalue(), "Recon_Report.xlsx")
                    
    elif user_pass != "":
        st.error("❌ Invalid Password")

if __name__ == "__main__":
    main()
