import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Professional Recon", layout="wide")

def main():
    st.title("📊 Advanced Sales Reconciliation")
    
    if 'authenticated' not in st.session_state: st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_pass = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            if user_pass == "Raman@2026":
                st.session_state.authenticated = True
                st.rerun()
    else:
        st.success("Welcome Raman Roy! 👋")
        
        col1, col2 = st.columns(2)
        with col1: tally_file = st.file_uploader("Tally File", type=['xlsx'])
        with col2: portal_file = st.file_uploader("Portal File", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("🚀 Run Advanced Reconciliation"):
                df_t = pd.read_excel(tally_file, header=1)
                df_p = pd.read_excel(portal_file)
                df_t.columns = ['Date', 'Name', 'Amount']
                df_p.columns = ['Date', 'Name', 'Amount']
                
                # Date Formatting
                df_t['Date'] = pd.to_datetime(df_t['Date'])
                df_p['Date'] = pd.to_datetime(df_p['Date'])
                
                # Logic: Name match + Date diff (10-15) + Amount diff (1-1500)
                merged = pd.merge(df_t, df_p, on='Name', suffixes=('_T', '_P'))
                
                merged['Date_Diff'] = (merged['Date_T'] - merged['Date_P']).dt.days.abs()
                merged['Amt_Diff'] = (merged['Amount_T'] - merged['Amount_P']).abs()
                
                # Categorization
                matches = merged[(merged['Date_Diff'] <= 15) & (merged['Amt_Diff'] <= 1500)]
                not_matches = merged[~((merged['Date_Diff'] <= 15) & (merged['Amt_Diff'] <= 1500))]
                
                # Formatting
                merged['Date_T'] = merged['Date_T'].dt.strftime('%d-%m-%Y')
                
                # Monthly/Yearly Summary
                merged['Month'] = pd.to_datetime(merged['Date_T'], format='%d-%m-%Y').dt.to_period('M')
                summary = merged.groupby('Month').agg({'Amount_T': 'sum', 'Amount_P': 'sum', 'Amt_Diff': 'sum'})
                
                st.write("### 📈 Monthly Analysis")
                st.dataframe(summary)
                
                st.write("### ✅ Matches (Criteria Met)")
                st.dataframe(matches[['Name', 'Date_T', 'Amount_T', 'Date_Diff', 'Amt_Diff']])
                
                st.write("### ❌ Not Matches / Review Needed")
                st.dataframe(not_matches)
                
                # Excel Download
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    summary.to_excel(writer, sheet_name='Summary')
                    matches.to_excel(writer, sheet_name='Matches')
                    not_matches.to_excel(writer, sheet_name='Not_Matches')
                st.download_button("📥 Download Final Professional Report", output.getvalue(), "Recon_Final.xlsx")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
