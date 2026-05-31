import streamlit as st
import pandas as pd
import io

# Password protection
PASSWORD = "Raman@2026"

def main():
    st.title("Sales Reconciliation Tool")
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        tally_file = st.file_uploader("Tally Excel file upload karein", type=['xlsx'])
        portal_file = st.file_uploader("Portal Excel file upload karein", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("Reconcile Karein"):
                # Files ko read karna (header=1 kyunki Tally mein 1st row title hai)
                df_tally = pd.read_excel(tally_file, header=1)
                df_portal = pd.read_excel(portal_file)
                
                # Column names fix karna
                df_tally.columns = ['Date', 'Party Name', 'Amount']
                df_portal.columns = ['Date', 'Party Name', 'Amount']
                
                # Merge logic
                merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                
                st.write("### Reconciliation Report:")
                st.dataframe(merged_df)
                
                # Download button
                excel_buffer = io.BytesIO()
                merged_df.to_excel(excel_buffer, index=False)
                st.download_button("Report Download karein", excel_buffer.getvalue(), "Report.xlsx")
                
    elif user_pass != "":
        st.error("Galat Password!")

if __name__ == "__main__":
    main()
