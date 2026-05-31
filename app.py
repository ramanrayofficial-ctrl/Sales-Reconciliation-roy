import streamlit as st
import pandas as pd
import io

PASSWORD = "Raman@2026"

def main():
    st.title("Sales Reconciliation Tool")
    
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        tally_file = st.file_uploader("Tally Sales Excel upload karein", type=['xlsx', 'csv'])
        portal_file = st.file_uploader("Portal Sales Excel upload karein", type=['xlsx', 'csv'])
        
        if tally_file and portal_file:
            if st.button("Reconcile Karein"):
                # Data read karna (header ko manually detect karne ki koshish)
                try:
                    # Tally file mein shayad upar 1 row title hai
                    df_tally = pd.read_excel(tally_file, skiprows=1) if tally_file.name.endswith('.xlsx') else pd.read_csv(tally_file, skiprows=1)
                    df_portal = pd.read_excel(portal_file) if portal_file.name.endswith('.xlsx') else pd.read_csv(portal_file)
                    
                    # Column ke naam force-fully set karna taaki column mismatch na ho
                    df_tally = df_tally.iloc[:, :3]
                    df_portal = df_portal.iloc[:, :3]
                    df_tally.columns = ['Date', 'Party Name', 'Amount']
                    df_portal.columns = ['Date', 'Party Name', 'Amount']
                    
                    # Date aur Amount format fix karna
                    df_tally['Date'] = pd.to_datetime(df_tally['Date'])
                    df_portal['Date'] = pd.to_datetime(df_portal['Date'])
                    df_tally['Amount'] = pd.to_numeric(df_tally['Amount'])
                    df_portal['Amount'] = pd.to_numeric(df_portal['Amount'])
                    
                    # Merge
                    merged_df = pd.merge(df_tally, df_portal, on=['Date', 'Party Name'], suffixes=('_Tally', '_Portal'))
                    merged_df['Difference'] = merged_df['Amount_Tally'] - merged_df['Amount_Portal']
                    
                    st.dataframe(merged_df)
                    
                    # Download
                    excel_buffer = io.BytesIO()
                    merged_df.to_excel(excel_buffer, index=False)
                    st.download_button("Report Download karein", excel_buffer.getvalue(), "Report.xlsx")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.write("Sahi columns nahi mile. Kripya check karein ki dono files mein Date, Party Name, aur Amount columns hain ya nahi.")
                    
    elif user_pass != "":
        st.error("Galat Password!")

if __name__ == "__main__":
    main()
