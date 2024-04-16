import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="hfcs",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded" 
)

list1 = []
file1 = st.file_uploader("Upload CSV file", type=['csv'])
access_token = st.text_input("Enter Access Token ")
authorization = st.text_input("Enter Authorization Token (Bearer token)")

if file1 and access_token and authorization:
    df = pd.read_csv(file1)

   
    st.write(df)
    list1 = []

    if not df.empty:
        api_url = 'https://intouch.mapmyindia.com/apis/api/entity'

        # Headers
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
            'access_token': access_token,
            'access_type': '1',
            'accountid': '3310923',
            'authorization': authorization,
            'content-type': 'application/json',
            'origin': 'https://intouch.mapmyindia.com',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'userid': '3475960'
        }

        # Iterate over DataFrame rows
        for index, row in df.iterrows():
            entity_id = row['Entity ID'] 
            col_2_value = row['col_2']
 #           col_4_value = row['col_4']

            # Data for PATCH request
            data = {
                "extendedData": {
                    "HFCS_Extended_DB_1703058763": {
                        "col_2": col_2_value
     #                   "col_4": col_4_value
                    }
                }
            }

            
            entity_url = f"{api_url}/{entity_id}/4"  # Correct URL construction

            # Make the PATCH request
            response = requests.patch(entity_url, headers=headers, json=data)
            list1.append(response)
            
            
            st.write(f"Entity ID: {entity_id}, Status Code: {response.status_code}")

st.write("Total Entity Update ", len(list1))
