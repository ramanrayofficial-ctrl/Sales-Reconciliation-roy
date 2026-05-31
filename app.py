import streamlit as st
import pandas as pd
# ... (baaki imports)

def main():
    st.title("📊 Sales Reconciliation")
    
    # Session state ka use karenge taaki password ek baar dalne par session bana rahe
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Agar password abhi tak sahi nahi dala hai, toh input dikhao
    if not st.session_state.authenticated:
        user_pass = st.text_input("Enter Password:", type="password")
        if st.button("Login"):
            if user_pass == "Raman@2026":
                st.session_state.authenticated = True
                st.rerun() # Page ko refresh karega
            else:
                st.error("❌ Invalid Password")
    
    # Agar password sahi ho gaya hai, toh password field hide ho jayegi
    # aur sirf file upload options dikhenge
    else:
        st.success("Welcome! Ab files upload karein.")
        
        col1, col2 = st.columns(2)
        with col1:
            tally_file = st.file_uploader("Tally Excel", type=['xlsx'])
        with col2:
            portal_file = st.file_uploader("Portal Excel", type=['xlsx'])
            
        # ... (baaki reconciliation code)
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
