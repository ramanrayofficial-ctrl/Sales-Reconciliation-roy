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
            if st.button("🚀 Process Data"):
                # Data Load
                df_t = pd.read_excel(tally_file, header=1)
                df_p = pd.read_excel(portal_file)
                
                df_t.columns = ['Date', 'Name', 'Tally Sales']
                df_p.columns = ['Date', 'Name', 'Portal Sales']
                
                # Date Processing (Ensure datetime objects)
                df_t['Date'] = pd.to_datetime(df_t['Date'])
                df_p['Date'] = pd.to_datetime(df_p['Date'])
                
                # Create helper columns for Display
                df_t['Tally Date'] = df_t['Date'].dt.strftime('%d-%m-%Y')
                df_p['Portal Date'] = df_p['Date'].dt.strftime('%d-%m-%Y')
                
                # Month columns for merging
                df_t['Month'] = df_t['Date'].dt.to_period('M')
                df_p['Month'] = df_p['Date'].dt.to_period('M')
                
                # Merge
                merged = pd.merge(df_t, df_p, on=['Month', 'Name'], suffixes=('_T', '_P'))
                
                # --- CORRECTED CALCULATION ---
                # Difference calculate karte waqt original datetime column ka use karein
                merged['Date_Diff'] = (merged['Date_T'] - merged['Date_P']).dt.days
                merged['Amt_Diff'] = merged['Tally Sales'] - merged['Portal Sales']
                
                # Columns for Display
                cols_to_show = ['Name', 'Tally Date', 'Tally Sales', 'Portal Date', 'Portal Sales', 'Date_Diff', 'Amt_Diff']
                
                # Matches/Not Matches based on absolute differences
                matches = merged[(merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500)]
                not_matches = merged[~((merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500))]
                
                # Monthly Analysis
                summary = merged.groupby('Month').agg({'Tally Sales': 'sum', 'Portal Sales': 'sum', 'Amt_Diff': 'sum'})
                
                st.write("### 📈 Monthly Analysis")
                st.dataframe(summary, height=200)
                
                st.write("### ✅ Matches")
                st.dataframe(matches[cols_to_show], height=400)
                
                st.write("### ❌ Not Matches")
                st.dataframe(not_matches[cols_to_show], height=400)
                
                # Download
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    summary.to_excel(writer, sheet_name='Summary')
                    matches.to_excel(writer, sheet_name='Matches', index=False)
                    not_matches.to_excel(writer, sheet_name='Not_Matches', index=False)
                st.download_button("📥 Download Final Report", output.getvalue(), "Recon_Final.xlsx")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
