# ... (Baaki code wahi rahega, bas 'Categorization' wale part ko aise update karein)

                # Date formatting (Time hatane ke liye)
                merged['Date_T'] = merged['Date_T'].dt.strftime('%d-%m-%Y')
                merged['Date_P'] = merged['Date_P'].dt.strftime('%d-%m-%Y')
                
                # Categorization
                matches = merged[(merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500)]
                not_matches = merged[~((merged['Date_Diff'].abs() <= 15) & (merged['Amt_Diff'].abs() <= 1500))]
                
                # UI Tables
                st.write("### 📈 Monthly Analysis")
                st.dataframe(summary, height=200)
                
                st.write("### ✅ Matches")
                # Yahan bhi headings clear kar di hain
                st.dataframe(matches[['Month', 'Name', 'Date_T', 'Tally Sales', 'Portal Sales', 'Amt_Diff']], height=300)
                
                st.write("### ❌ Not Matches")
                # Yahan 'Date_T' aur 'Date_P' dono dikhayenge taaki comparison easy ho
                st.dataframe(not_matches[['Month', 'Name', 'Date_T', 'Date_P', 'Tally Sales', 'Portal Sales', 'Amt_Diff']], height=300)
                
# ... (Download wala hissa wahi rahega)
