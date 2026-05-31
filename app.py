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
                
                # Normalize Dates
                df_t['Date'] = pd.to_datetime(df_t['Date']).dt.normalize()
                df_p['Date'] = pd.to_datetime(df_p['Date']).dt.normalize()
                
                # Merge based on Name (100% Match) and Month
                df_t['Month'] = df_t['Date'].dt.to_period('M')
                df_p['Month'] = df_p['Date'].dt.to_period('M')
                
                # Strict Inner Merge on Name and Month
                merged = pd.merge(df_t, df_p, on=['Month', 'Name'], suffixes=('_T', '_P'))
                
                # Absolute Differences
                merged['Date_Diff'] = (merged['Date_T'] - merged['Date_P']).dt.days.abs()
                merged['Amt_Diff'] = (merged['Tally Sales'] - merged['Portal Sales']).abs()
                
                # MATCHING CRITERIA: 
                # 1. Name already 100% matched by merge
                # 2. Date diff <= 15
                # 3. Amount diff <= 1500
                is_match = (merged['Date_Diff'] <= 15) & (merged['Amt_Diff'] <= 1500)
                
                matches = merged[is_match].copy()
                not_matches = merged[~is_match].copy()
                
                # Formatting Display
                merged['Tally Date'] = merged['Date_T'].dt.strftime('%d-%m-%Y')
                merged['Portal Date'] = merged['Date_P'].dt.strftime('%d-%m-%Y')
                cols_to_show = ['Name', 'Tally Date', 'Tally Sales', 'Portal Date', 'Portal Sales', 'Date_Diff', 'Amt_Diff']
                
                st.write("### ✅ Matches")
                st.dataframe(matches[cols_to_show], height=400)
                
                st.write("### ❌ Not Matches")
                st.dataframe(not_matches[cols_to_show], height=400)
                
                # Download
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    matches[cols_to_show].to_excel(writer, sheet_name='Matches', index=False)
                    not_matches[cols_to_show].to_excel(writer, sheet_name='Not_Matches', index=False)
                st.download_button("📥 Download Final Report", output.getvalue(), "Recon_Final.xlsx")

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
