import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Sales Recon", layout="centered")

def main():
    st.title("📊 Sales Reconciliation Tool")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        user_pass = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            if user_pass == "Raman@2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid Password")
    else:
        # --- YE RAHI AAPKI CUSTOM GREETING ---
        st.success("Welcome Raman Roy! 👋")
        
        tally_file = st.file_uploader("Tally Excel upload karein", type=['xlsx'])
        portal_file = st.file_uploader("Portal Excel upload karein", type=['xlsx'])
        
        if tally_file and portal_file:
            if st.button("🚀 Process & Reconcile"):
                with st.spinner('Data process ho raha hai...'):
                    df_tally = pd.read_excel(tally_file, header=1)
                    df_portal = pd.read_excel(portal_file)
                    
                    df_tally.columns = ['Date', 'Party Name', 'Amount']
                    df_portal.columns = ['Date', 'Party Name', 'Amount']
                    
                    df_tally['Date'] = pd.to_datetime(df_tally['Date'])
                    df_portal['Date'] = pd.to_datetime(df_portal['Date'])
                    
                    # Merge Logic
                    merged = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                    merged['Difference'] = merged['Amount_Tally'] - merged['Amount_Portal']
                    
                    # Categories
                    matches = merged[merged['Difference'] == 0]
                    not_matches = merged[merged['Difference'] != 0]
                    
                    # Monthly Summary
                    merged['Month'] = merged['Date'].dt.strftime('%B-%Y')
                    summary = merged.groupby('Month').agg({'Amount_Tally': 'sum', 'Amount_Portal': 'sum', 'Difference': 'sum'})
                    
                    st.write("### 📊 Monthly Summary")
                    st.dataframe(summary)
                    st.write(f"✅ Matched: {len(matches)} | ❌ Not Matched: {len(not_matches)}")
                    
                    # Download 3 Sheets
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        summary.to_excel(writer, sheet_name='Monthly_Summary')
                        matches.to_excel(writer, sheet_name='Matches')
                        not_matches.to_excel(writer, sheet_name='Unmatched')
                    
                    st.download_button("📥 Download Final Report (3 Sheets)", output.getvalue(), "Reconciliation_Final.xlsx")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
