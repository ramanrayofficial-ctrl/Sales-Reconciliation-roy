import streamlit as st
import pandas as pd
import io

PASSWORD = "Raman@2026"

def main():
    st.title("Sales Reconciliation Tool")
    
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        tally_file = st.file_uploader("Tally Sales Excel upload karein", type=['xlsx'])
        portal_file = st.file_uploader("Portal Sales Excel upload karein", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("Reconcile Karein"):
                df_tally = pd.read_excel(tally_file)
                df_portal = pd.read_excel(portal_file)
                
                # Column mapping
                df_tally.columns = ['Date', 'Party Name', 'Amount']
                df_portal.columns = ['Date', 'Party Name', 'Amount']
                
                merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                
                st.dataframe(merged_df)
                
                # Excel Download
                excel_buffer = io.BytesIO()
                merged_df.to_excel(excel_buffer, index=False)
                st.download_button("Excel mein Download karein", excel_buffer.getvalue(), "Report.xlsx", "application/vnd.ms-excel")
    elif user_pass != "":
        st.error("Galat Password!")

if __name__ == "__main__":
    main()
