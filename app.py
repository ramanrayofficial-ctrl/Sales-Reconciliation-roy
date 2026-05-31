        if tally_file and portal_file:
            if st.button("🚀 Process Month-Wise"):
                # Data Load
                df_t = pd.read_excel(tally_file, header=1)
                df_p = pd.read_excel(portal_file)
                
                df_t.columns = ['Date', 'Name', 'Tally Sales']
                df_p.columns = ['Date', 'Name', 'Portal Sales']
                
                # --- YE WALA HISSA UPDATE KAREIN ---
                # Pehle date ko datetime mein badlein
                df_t['Date'] = pd.to_datetime(df_t['Date'])
                df_p['Date'] = pd.to_datetime(df_p['Date'])
                
                # Phir String mein badlein taaki time hat jaye
                df_t['Date_Str'] = df_t['Date'].dt.strftime('%d-%m-%Y')
                df_p['Date_Str'] = df_p['Date'].dt.strftime('%d-%m-%Y')
                
                # Month calculation
                df_t['Month'] = df_t['Date'].dt.to_period('M').astype(str)
                df_p['Month'] = df_p['Date'].dt.to_period('M').astype(str)
                
                # Merge (Ab Date_Str ka use karein display ke liye)
                merged = pd.merge(df_t, df_p, on=['Month', 'Name'], suffixes=('_T', '_P'))
                
                # Calculations
                merged['Date_Diff'] = (merged['Date_T'] - merged['Date_P']).dt.days
                merged['Amt_Diff'] = merged['Tally Sales'] - merged['Portal Sales']
                
                # Categorization
                matches = merged[(merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500)]
                not_matches = merged[~((merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500))]
                
                # Display mein Date_Str dikhayein
                st.write("### 📈 Monthly Analysis")
                st.dataframe(summary, height=200)
                
                st.write("### ✅ Matches")
                # Yahan Date_T_Str aur Date_P_Str ka use karein
                st.dataframe(matches[['Month', 'Name', 'Date_T_Str', 'Tally Sales', 'Portal Sales', 'Amt_Diff']], height=300)
                
                st.write("### ❌ Not Matches")
                st.dataframe(not_matches[['Month', 'Name', 'Date_T_Str', 'Date_P_Str', 'Tally Sales', 'Portal Sales', 'Amt_Diff']], height=300)
