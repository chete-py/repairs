import streamlit as st
import pandas as pd
import gspread
import plotly as px
from google.oauth2 import service_account
import plotly.graph_objects as go
import base64


# def check_password():
#     """Returns `True` if the user had a correct password."""

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if (
#             st.session_state["username"] in st.secrets["passwords"]
#             and st.session_state["password"]
#             == st.secrets["passwords"][st.session_state["username"]]
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store username + password
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False

#     if "password_correct" not in st.session_state:
#         # First run, show inputs for username + password.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         st.error("Invalid Credentials")
#         return False
#     else:
#         # Password correct.
#         return True

# if check_password():

# Define your Google Sheets credentials JSON file (replace with your own)
credentials_path = 'atlantean-app-402209-ff6eeccdec5b.json'

# Authenticate with Google Sheets using the credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])

# Authenticate with Google Sheets using gspread
gc = gspread.authorize(credentials)

# Your Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/1tv3F0svnneK95tHbAA4l6OotcrD87A6bWXXlLo2lLxg/edit#gid=0"

# Open the Google Sheets spreadsheet
worksheet = gc.open_by_url(url).worksheet("repairs")


    # Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)
st.sidebar.markdown("Navigation Pane")
    
# Main Streamlit app code
def main():

    view = st.sidebar.radio("Select", ["Dashboard", "New Update", "Records"])

    if view == "Dashboard":
        st.subheader("REPAIRS TRACKER")

        # Read data from the Google Sheets worksheet
        data = worksheet.get_all_values()

        # Prepare data for Plotly
        headers = data[0]
        data = data[1:]
        df = pd.DataFrame(data, columns=headers)  # Convert data to a DataFrame
        
        # Assuming your DataFrame is named 'df'
        df['Delete'] = [''] * len(df)

        # Convert the "Amount Collected" column to numeric
        #df['REPAIR AMOUNT'] = df['REPAIR AMOUNT'].str.replace(',', '').astype(float)

        freq_garage = df['REPAIRER'].mode().values[0]

        count_garage = df[df["REPAIRER"] == freq_garage].shape[0]

    
        freq_assessor = df['ASSESSOR '].mode().values[0]
        count_assessor = df[df["ASSESSOR "] == freq_assessor].shape[0]

        
        # Remove non-numeric characters and convert the column to numeric
        df["REPAIR AMOUNT"] = pd.to_numeric(df["REPAIR AMOUNT"].str.replace(r'[^0-9.]', '', regex=True), errors='coerce')

        agg_repair = df.groupby('REPAIRER')['REPAIR AMOUNT'].sum().reset_index()

        final_agg = agg_repair.sort_values(by='REPAIR AMOUNT', ascending=False).head(5)

        top = df.sort_values(by='REPAIR AMOUNT', ascending=False).head(5)



        # Now, you can perform the sum operation
        # agg = df["REPAIR AMOUNT"].sum()

        agg = df["REPAIR AMOUNT"].sum()

        total_amount = "Ksh. {:,.0f}".format(agg)


    
        # Get the person with the highest sum
        # highest_garage = result.head(8)  

        # print(highest_garage)                    
        


        st.markdown(
            f'<div style= "display: flex; flex-direction: row;">'  # Container with flex layout
            f'<div style="background-color: #f19584; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
            f'<strong style="color: black; font-size: 12px">MOST FREQUENT GARAGE</strong> <br>'  
            f"{freq_garage}<br>"
            f"{count_garage} times<br>"
            f'</div>'
            # f'<strong style="color: black; font-size: 12px">TOP GARAGE</strong> <br>'  
            # f"<br>"
            # f"{highest_garage}<br>"
            # f'</div>'
            f'<div style="background-color: #FFE599; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
            f'<strong style="color: black; font-size: 12px">MOST FREQUENT ASSESSOR</strong> <br>'
            f"{freq_assessor}<br>"
            f"{count_assessor} times<br>"
            f'</div>'                
            f'<div style="background-color: #a8e4a0; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
            f'<strong style="color: black; font-size: 12px">CUMULATIVE REPAIR AMOUNT</strong> <br>'  
            f"<br>"
            f"{total_amount}<br>"
            f'</div>'                
            f'</div>',
            unsafe_allow_html=True
        )

        # Create a Plotly bar graph
        #fig = px.bar(x=x_data, y=y_data, labels={'x': 'Garage', 'y': 'Repair Amount'})

        
        fig = go.Figure(data=[go.Bar(
            x= final_agg["REPAIRER"],
            y= final_agg["REPAIR AMOUNT"]        
            )])

        fig.update_layout(title={'text': 'REPAIR AMOUNT THE FREQUENT GARAGES', 'x': 0.375, 'xanchor': 'center'}) 

        # Display the Plotly bar graph in Streamlit
        st.markdown("")
        st.plotly_chart(fig)

        

        # Create a pie chart using Plotly
        fig_pie = go.Figure(data=[go.Pie(labels=df["OUTCOME"])])

        # Set the chart title
        fig_pie.update_layout(title_text="COMPOSITION OF OUTCOME DISTRIBUTION")

        # Show the pie chart
        st.plotly_chart(fig_pie)

        st.markdown('TOP FIVE REPAIR PAYOUTS')
        st.write(top, unsafe_allow_html=True)

        

    if view == "New Update":
            # Add the dashboard elements here
        st.subheader("REPAIRS TRACKER")
    
        # Create form fields for user input   

        reg = st.text_input("Registration Number")

        claim = st.text_input("Claim Number") 
    
        repairer = st.selectbox("Repairer", ["SIMBA", "SAGOO", "LEAKEYS", "COMBINE", "MOTION", "AUTOEXPRESS", "KHALSA", "JOGINDERS", "WINDSCREEN", "C.I.L", "T.B.A", "N/A"])
    
        assessor = st.selectbox("Assessor", ["EXPRESS", "KEVO", "NOT ASSESSED", "TPPD", "T.B.A"])

        assessor_appointed = st.text_input("Date Assessor Appointed")  

        report_received = st.text_input("Date Report Received")  

        outcome = st.selectbox("Claim Outcome", ["REPAIRABLE", "THIRD PARTY PURPOSES", "PENDING", "WRITE-OFF", "BELOW EXCESS", "UNDER INVESTIGATION", "CLAIM DECLINED", "RELEASED"])

        date_authorized = st.text_input("Date Repair Authorized")

        repair_amount = st.text_input("Repair Amount") 
    
        release_date = st.text_input("Release Date")  
    
    
    
            # Check if the user has entered data and submitted the form
        if st.button("Submit"):
            
            # Create a new row of data to add to the Google Sheets spreadsheet
            new_data = [reg, claim, repairer, assessor, assessor_appointed, report_received, outcome, date_authorized, repair_amount, release_date]
    
            # Append the new row of data to the worksheet
            worksheet.append_row(new_data) 
    
            st.success("Data submitted successfully!")
    
    
    elif view == "Records":
            # Show the saved DataFrame here
        data = worksheet.get_all_values()
        headers = data[0]
        data = data[1:]
        df = pd.DataFrame(data, columns=headers)  # Convert data to a DataFrame
        st.subheader("RECORDS")

        # Get the unique reviewer names from the DataFrame
        unique_outcome = df['OUTCOME'].unique()

            # Create a dropdown to select a reviewer with "All" option
        selected = st.selectbox("Filter by Outcome:", ["All"] + list(unique_outcome))

        if selected != "All":
            # Filter the DataFrame based on the selected reviewer
            final_df = df[df['OUTCOME'] == selected]

        else:
            # If "All" is selected, show the entire DataFrame
            final_df = df

        selected_option = st.selectbox("Filter by Date:", ["All", "With Date", "Without Date"])

        if selected_option == "All":
           
            final_df = df
        
        elif selected_option == "With Date":
            # Filter the DataFrame to include rows with dates
            final_df = df[df['date_authorized'].notnull() == selected_option]
        
        elif selected_option == "Without Date":
            # Filter the DataFrame to include rows without dates (blanks)
            final_df = df[df['date_authorized'].isnull() == selected_option]    
    
        edited_df = st.data_editor(final_df)
    
        # Add a button to update Google Sheets with the changes
        if st.button("Update Google Sheets"):
            worksheet.clear()  # Clear the existing data in the worksheet
            worksheet.update([edited_df.columns.tolist()] + edited_df.values.tolist())
    
        # Add a button to download the filtered data as a CSV
        if st.button("Download CSV"):
            csv_data = edited_df.to_csv(index=False, encoding='utf-8')
            b64 = base64.b64encode(csv_data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="repair_report.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)              

if __name__ == "__main__":
    main()
