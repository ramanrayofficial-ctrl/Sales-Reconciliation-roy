import streamlit as st
import pandas as pd
import io

# Professional UI Configuration
st.set_page_config(page_title="Professional Sales Reconciliation", layout="wide")

def main():
    st.title("📊 Professional Sales Reconciliation Tool")
    st.markdown("---")
    
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_pass = st.text_input("Enter Access Password:", type="password")
        if st.button("Login"):
            if user_pass == "Raman@2026":
                st.session_state.authenticated = True
                st.rerun()
    else:
        st.success("Welcome Raman Kumar Ray! Session Active.")
        
        col1, col2 = st.columns(2)
        with col1: tally_file = st.file_uploader("Upload Tally Sales Data", type=['xlsx'])
        with col2: portal_file = st.file_uploader("Upload Portal Sales Data", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("🚀 Execute Reconciliation"):
                # Data Loading
                df_t = pd.read_excel(tally_file)
                df_p = pd.read_excel(portal_file)
                
                # Column Naming (Ensure 'Date', 'Party Name', 'Amount' structure)
                df_t.columns = ['Date', 'Party Name', 'Amount']
                df_p.columns = ['Date', 'Party Name', 'Amount']
                
                # Normalization
                df_t['Date'] = pd.to_datetime(df_t['Date']).dt.normalize()
                df_p['Date'] = pd.to_datetime(df_p['Date']).dt.normalize()
                
                # Merging on Party Name (100% Match)
                merged = pd.merge(df_t, df_p, on='Party Name', suffixes=('_Tally', '_Portal'))
                
                # Logic Calculations
                merged['Date_Diff'] = (merged['Date_Tally'] - merged['Date_Portal']).dt.days.abs()
                merged['Amt_Diff'] = (merged['Amount_Tally'] - merged['Amount_Portal']).abs()
                
                # Strict Criteria: Date 1-5 days, Amount 1-200
                is_match = (merged['Date_Diff'] >= 1) & (merged['Date_Diff'] <= 5) & \
                           (merged['Amt_Diff'] >= 1) & (merged['Amt_Diff'] <= 200)
                
                matches = merged[is_match].copy()
                not_matches = merged[~is_match].copy()
                
                # Display Formatting
                cols = ['Party Name', 'Date_Tally', 'Amount_Tally', 'Date_Portal', 'Amount_Portal', 'Date_Diff', 'Amt_Diff']
                
                st.markdown("### ✅ Verified Matches")
                st.dataframe(matches[cols], use_container_width=True)
                
                st.markdown("### ❌ Discrepancy Report (Not Matches)")
                st.dataframe(not_matches[cols], use_container_width=True)
                
                # Export Button
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    matches[cols].to_excel(writer, sheet_name='Matches', index=False)
                    not_matches[cols].to_excel(writer, sheet_name='Not_Matches', index=False)
                st.download_button("📥 Download Final Reconciliation Report", output.getvalue(), "Sales_Recon_Report.xlsx")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
