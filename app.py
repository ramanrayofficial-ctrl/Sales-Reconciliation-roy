import streamlit as st
import pandas as pd

# Password Set kiya hai
PASSWORD = "Raman@2026"

def main():
    st.title("Sales Reconciliation Tool")
    
    # Password Check
    user_pass = st.text_input("Password dalein:", type="password")
    
    if user_pass == PASSWORD:
        st.success("Password Sahi hai! Ab aap files upload kar sakte hain.")
        
        # Yahan aapka baki ka code aayega
        tally_file = st.file_uploader("Tally file upload karein", type=['xlsx'])
        portal_file = st.file_uploader("Portal file upload karein", type=['xlsx'])
        
        if tally_file and portal_file:
            st.write("Files upload ho gayi hain! (Abhi reconciliation logic add karna baki hai)")
            
    elif user_pass != "":
        st.error("Galat Password! Kripya sahi password dalein.")

if __name__ == "__main__":
    main()
    
