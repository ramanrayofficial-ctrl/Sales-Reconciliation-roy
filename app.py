import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Professional Recon Report", layout="wide")

def main():
    st.title("📊 Sales Reconciliation Report Generator")
    
    # Login Logic
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False
    if not st.session_state.authenticated:
        if st.text_input("Enter Password:", type="password") == "Raman@2026":
            st.session_state.authenticated = True
            st.rerun()
        return

    # File Uploads
    col1, col2 = st.columns(2)
    with col1: tally_file = st.file_uploader("Upload Tally File", type=['xlsx'])
    with col2: portal_file = st.file_uploader("Upload Portal File", type=['xlsx'])

    if tally_file and portal_file:
        if st.button("🚀 Generate Professional Report"):
            df_t = pd.read_excel(tally_file)
            df_p = pd.read_excel(portal_file)
            
            # Data Cleaning (Mapping your columns)
            df_t.columns = ['Date', 'Party Name', 'Amount']
            df_p.columns = ['Date', 'Party Name', 'Amount']
            
            df_t['Date'] = pd.to_datetime(df_t['Date'], errors='coerce').dt.normalize()
            df_p['Date'] = pd.to_datetime(df_p['Date'], errors='coerce').dt.normalize()
            
            # Logic: Merge & Threshold Calculation
            merged = pd.merge(df_t, df_p, on='Party Name', suffixes=('_Tally', '_Portal'))
            merged['Date_Diff'] = (merged['Date_Tally'] - merged['Date_Portal']).dt.days.abs()
            merged['Amt_Diff'] = (merged['Amount_Tally'] - merged['Amount_Portal']).abs()
            
            # Filter criteria: Date (1-5), Amount (1-200)
            is_match = (merged['Date_Diff'] >= 1) & (merged['Date_Diff'] <= 5) & \
                       (merged['Amt_Diff'] >= 1) & (merged['Amt_Diff'] <= 200)
            
            matches = merged[is_match].copy()
            not_matches = merged[~is_match].copy()
            
            # Professional Summary Calculation
            summary = pd.DataFrame({
                'Metric': ['Total Transactions', 'Matched', 'Not Matched', 'Total Amount Diff'],
                'Value': [len(merged), len(matches), len(not_matches), merged['Amt_Diff'].sum()]
            })

            # Displaying in Dashboard Style
            st.markdown("### 📈 Summary Dashboard")
            st.table(summary)
            
            st.markdown("### 📑 Detailed Reconciliation Ledger")
            st.dataframe(merged, use_container_width=True)
            
            st.markdown("### ⚠️ Not Matched Report")
            st.dataframe(not_matches, use_container_width=True)
            
            # Download Multi-sheet Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                summary.to_excel(writer, sheet_name='Summary', index=False)
                merged.to_excel(writer, sheet_name='Reconciliation Ledger', index=False)
                not_matches.to_excel(writer, sheet_name='Not Matched Report', index=False)
            st.download_button("📥 Download Full Report", output.getvalue(), "Final_Reconciliation_Report.xlsx")

if __name__ == "__main__":
    main()
