import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Sales Recon", layout="centered")

def main():
    st.title("📊 Sales Reconciliation")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_pass = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            if user_pass == "Raman@2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid Password")
    else:
        st.success("Welcome! Ab files upload karein.")
        
        tally_file = st.file_uploader("Tally Excel", type=['xlsx'])
        portal_file = st.file_uploader("Portal Excel", type=['xlsx'])
        
        if tally_file and portal_file:
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
                    
                    output = io.BytesIO()
                    merged_df.to_excel(output, index=False)
                    st.download_button("📥 Download Report", output.getvalue(), "Recon_Report.xlsx")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
