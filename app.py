    # ... (Login wala session state code upar rahega)

    else:
        st.success("Welcome! Ab files upload karein.")
        
        # Files Upload Section
        tally_file = st.file_uploader("Tally Excel", type=['xlsx'])
        portal_file = st.file_uploader("Portal Excel", type=['xlsx'])
        
        # --- NAYA CHANGE YAHAN HAI ---
        # Sirf tabhi "Reconcile" button dikhega jab dono files upload ho jayengi
        if tally_file is not None and portal_file is not None:
            if st.button("🚀 Reconcile Data Now"):
                # Yahan aapka processing wala code aayega
                with st.spinner('Data process ho raha hai...'):
                    df_tally = pd.read_excel(tally_file, header=1)
                    df_portal = pd.read_excel(portal_file)
                    
                    # ... (baaki logic jo humne pehle likhi thi)
                    st.success("Reconciliation Complete!")
                    st.dataframe(merged_df)
                    # ... (download button)
        
        # Logout button
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
