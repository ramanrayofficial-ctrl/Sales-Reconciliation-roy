import streamlit as st
import pandas as pd
import io

PASSWORD = "Raman@2026"

def main():
    st.title("Sales Reconciliation Tool")
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        tally_file = st.file_uploader("Tally Sales upload karein", type=['xlsx', 'csv'])
        portal_file = st.file_uploader("Portal Sales upload karein", type=['xlsx', 'csv'])
        
        if tally_file and portal_file:
            if st.button("Reconcile Karein"):
                # Files Read karna
                df_tally = pd.read_excel(tally_file, skiprows=1) if tally_file.name.endswith('.xlsx') else pd.read_csv(tally_file, skiprows=1)
                df_portal = pd.read_excel(portal_file) if portal_file.name.endswith('.xlsx') else pd.read_csv(portal_file)
                
                # Column names ko saaf karna (space hataana)
                df_tally.columns = df_tally.columns.str.strip()
                df_portal.columns = df_portal.columns.str.strip()
                
                # Sahi columns select karna (Date, Party Name, Amount)
                # Apni files ke hisab se mapping set kar rahe hain
                df_tally = df_tally[['DATE', 'PARTY NAME', 'AMOUNT']]
                df_portal = df_portal[['DATE', 'PARTY NAME', 'AMOUNT']]
                
                # Renaming
                df_tally.columns = ['Date', 'Party Name', 'Amount']
                df_portal.columns = ['Date', 'Party Name', 'Amount']
                
                # Reconciliation
                merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                
                st.dataframe(merged_df)
                
                # Download
                excel_buffer = io.BytesIO()
                merged_df.to_excel(excel_buffer, index=False)
                st.download_button("Report Download karein", excel_buffer.getvalue(), "Report.xlsx")
                
    elif user_pass != "":
        st.error("Galat Password!")

if __name__ == "__main__":
    main()
