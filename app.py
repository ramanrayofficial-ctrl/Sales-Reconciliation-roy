import streamlit as st
import pandas as pd
import io
from datetime import datetime

PASSWORD = "Raman@2026"

def main():
    st.set_page_config(page_title="Sales Recon Tool", layout="wide")
    st.title("📊 Sales Reconciliation Professional Tool")
    
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        col1, col2 = st.columns(2)
        with col1:
            tally_file = st.file_uploader("Tally Sales File (.xlsx)", type=['xlsx'])
        with col2:
            portal_file = st.file_uploader("Portal Sales File (.xlsx)", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("🚀 Reconcile Data"):
                # Data Processing
                df_tally = pd.read_excel(tally_file, header=1)
                df_portal = pd.read_excel(portal_file)
                
                # Column Cleaning
                df_tally.columns = ['Date', 'Party Name', 'Amount']
                df_portal.columns = ['Date', 'Party Name', 'Amount']
                
                # Date aur Amount fix karna
                df_tally['Date'] = pd.to_datetime(df_tally['Date']).dt.strftime('%d-%m-%Y')
                df_portal['Date'] = pd.to_datetime(df_portal['Date']).dt.strftime('%d-%m-%Y')
                
                # Merge
                merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                
                # Professional Display
                st.write("### ✅ Reconciliation Summary")
                st.dataframe(merged_df.style.format({'Amount_Tally': '{:,.2f}', 'Amount_Portal': '{:,.2f}', 'Difference': '{:,.2f}'}))
                
                # Excel Download with formatting
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    merged_df.to_excel(writer, index=False, sheet_name='Report')
                
                st.download_button(
                    label="📥 Download Professional Report",
                    data=output.getvalue(),
                    file_name=f"Recon_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
    elif user_pass != "":
        st.error("❌ Galat Password!")

if __name__ == "__main__":
    main()
