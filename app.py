import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Reconciler", layout="wide")
st.title("🔄 Universal Sales Reconciliation Tool")

tally_file = st.file_uploader("Tally Sales Sheet Upload karein", type=['xlsx'])
portal_file = st.file_uploader("Portal Sales Sheet Upload karein", type=['xlsx'])

if tally_file and portal_file:
    if st.button("Reconcile Karein"):
        df_tally = pd.read_excel(tally_file)
        df_portal = pd.read_excel(portal_file)
        
        # Simple Logic: Data show karna
        st.write("Dono file upload ho gayi hai! Logic yahan add hoga.")
        st.success("Reconciliation process shuru ho gaya hai.")
        