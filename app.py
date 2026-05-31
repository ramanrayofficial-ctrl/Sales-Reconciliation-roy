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
                
                # Date format fix (Time hatane ke liye)
                df_t['Date'] = pd.to_datetime(df_t['Date']).dt.normalize()
                df_p['Date'] = pd.to_datetime(df_p['Date']).dt.normalize()
                
                # Merge
                merged = pd.merge(df_t, df_p, on='Name', suffixes=('_T', '_P'))
                
                # Difference Calculation (Plus/Minus sahi aayega)
                merged['Date_Diff'] = (merged['Date_T'] - merged['Date_P']).dt.days
                merged['Amt_Diff'] = merged['Amount_T'] - merged['Amount_P'] 
                
                # Categorization based on logic
                matches = merged[(merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500)]
                not_matches = merged[~((merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500))]
                
                # Monthly Summary
                merged['Month'] = merged['Date_T'].dt.to_period('M').astype(str)
                summary = merged.groupby('Month').agg({'Amount_T': 'sum', 'Amount_P': 'sum', 'Amt_Diff': 'sum'})
                
                # UI Tables (Scrollable)
                st.write("### 📈 Monthly Analysis")
                st.dataframe(summary, height=200)
                
                st.write("### ✅ Matches (Diff within range)")
                st.dataframe(matches[['Name', 'Date_T', 'Amount_T', 'Date_Diff', 'Amt_Diff']], height=300)
                
                st.write("### ❌ Not Matches / Review")
                st.dataframe(not_matches, height=300)
                
                # Download
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
