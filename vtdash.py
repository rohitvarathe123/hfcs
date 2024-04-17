
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from streamlit_folium import folium_static
import folium
import json
from streamlit_player import st_player
st.set_page_config(
    page_title="VT API Response",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded" 
)



url = "https://www.vtapi.in:7820/vtapi/loginForApp"

payload = json.dumps({
  "loginName": "INGT",
  "loginPwd": "c976be0d9b888894754046d0c89b062f"
})
headers = {
  'lang': 'en_us',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
tokentxt = response.json()
token = tokentxt['data']['token']
if token:
    st.title("Welcome To Video Telematics API")
else:
    st.title("Login Failed")

response_list = []

# Function to make API requests and display response in Streamlit
def make_api_request(plate_no_value, mch):
    url = 'https://vtapi.in:7800/api/media/subscribe'
    headers = {'Content-Type': 'application/json'}

    data = {
        "auth_code": "sa",
        "client_id": 0,
        "plate_no": plate_no_value,
        "dev_id": 0,
        "mch": mch,
        "st": 0,
        "mtype": 3,
        "device_type": 0,
        "dev_network": 1,
        "intranet": 0
    }

    st.write(f"Channel {mch}\n")
    
    try:
        with st.spinner("Fetching data..."):
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        st.error(f"Error during API request: {e}")
        return

    st.write(f"Status Code: {response.status_code}")
    st.json(response.json())
    data = response.json()
    flvurl = data.get("flvurl","hlsurl")
    hlsurl = data.get("hlsurl")
    st.write(flvurl,hlsurl)
    st_player(hlsurl)
    response_list.append(hlsurl)









#plate_no_value = st.selectbox("Select Plate Number", plate_numbers, index=1)
plate_no_value = st.text_input("Enter Custom Plate Number")

current_time = datetime.now() - timedelta(hours=24)
start_time_input = st.text_input("Enter start Time (YYYY-MM-DD HH:MM:SS)", current_time.strftime('%Y-%m-%d %H:%M:%S'))
end_time_input = st.text_input("Enter End Time (YYYY-MM-DD HH:MM:SS)", (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'))

mch_list = [1, 2, 3, 4]

st.title('Live Streaming Response')
cols = st.columns(len(mch_list))

for i, ch in enumerate(mch_list):
    with cols[i]:
        make_api_request(plate_no_value, ch)
        st.write("---")
st.write(response_list)
cols = st.columns(len(response_list))  # Creating columns based on the length of response_list

for i, (hls, channel) in enumerate(zip(response_list, mch_list)):
    with cols[i]:
        st.video(hls)
        st.write(channel)


        
#=====================  =================================================================   =================================================================
st.title('History API Response')
#current_time2 = datetime.now() - timedelta(minutes=60)
#default_start_time = current_time2.strftime('%Y-%m-%d %H:%M:%S')
#
#current_time3 = datetime.now() - timedelta(minutes=55)
#default_end_time = current_time3.strftime('%Y-%m-%d %H:%M:%S')
#
#h_start_time = st.text_input("Enter start Time (YYYY-MM-DD HH:MM:SS)", default_start_time)
#h_end_time = st.text_input("Enter End Time (YYYY-MM-DD HH:MM:SS)", default_end_time)
#
#st.success(f"History Video Start Time : {h_end_time}")
#st.success(f"History Video End Time : {h_start_time}")

current_date = datetime.now() - timedelta(minutes=30)
current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
st.write(f"Current Date: {current_date_str}")

time_difference_options = ['2 min', '5 min', '10 min', '30 min', '60 min', '1 hour']
time_difference = st.selectbox("Select Time Difference:", time_difference_options)

time_difference_mapping = {
    '2 min': 2,
    '5 min': 5,
    '10 min': 10,
    '30 min': 30,
    '60 min': 60,
    '1 hour': 60
}

delta = timedelta(minutes=time_difference_mapping[time_difference])
start_date = current_date - delta
start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
st.write(f"Start Date: {start_date_str}")
st.write(f"End Date: {current_date_str}")

def historyapi(plate_no_value, mch):
    url = 'https://vtapi.in:7800/api/media/subscribe'
    headers = {'Content-Type': 'application/json'}


    data = {
        "auth_code": "sa",
        "client_id": 0,
        "dev_id": 0,
        "plate_no": plate_no_value,
        "mch": mch,
        "mtype": 3,
        "bs_type": 1,
        "device_type": 0,
        "btm": start_date_str,
        "etm": current_date_str,
        "dur": 15843,
        "store_type": 0,
        "playback_mode": 0,
        "ratio": 0,
        "Dev_network": 1,
        "Intranet": 0
    }
    st.write(f"Channel {mch}\n")
    
    try:
        with st.spinner("Fetching data..."):
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        st.error(f"Error during API request: {e}")
        return

    st.write(f"Status Code: {response.status_code}")
    st.json(response.json())
    data = response.json()
    flvurl = data.get("flvurl","hlsurl")
    hlsurl = data.get("hlsurl")
    st.write(flvurl,hlsurl)
    st_player(hlsurl, key=widget_key)



cols = st.columns(len(mch_list))
for i, ch in enumerate(mch_list):
    with cols[i]:
        widget_key = f"player_{ch}"
        historyapi(plate_no_value, ch)
        st.write("---")





##==========================================================================================================
st.title('Get Vehicle ID API Response')

url = 'https://www.vtapi.in:7820/vtapi/vehicleTree/getVehicleInfoForReport'
headers = {
    'lang': 'en_us',
    'Content-Type': 'application/json'
}
data = {
    'lpno': plate_no_value,
    'pageNo': 1,
    'limitNum': 10
}

response = requests.post(url, headers=headers, json=data)
vehid = response.json()
vehicleid = vehid["data"][0]["vehicleId"]
st.write("VehicleId ",vehicleid)
st.write(response.json())


st.title('Get Last Posstion of Vehicle API Response')
import requests

url = 'https://www.vtapi.in:7820/vtapi/vehicleMonitor/getPositionData'
headers = {
    'lang': 'en_us',
    'Content-Type': 'application/json',
}

data = {
    'vehicleIdList': [vehicleid]
}

# Sending POST request
response = requests.post(url, headers=headers, json=data)

# Checking the response
if response.status_code == 200:
    st.write("Request successful", response)
    st.write("Response:")
    st.write(response.json())
    ij_data = response.json()
    
    # Extract values for 'i' and 'j'
    j_value = ij_data['data']['gpsInfoList'][0]['i']
    i_value = ij_data['data']['gpsInfoList'][0]['j']

    # Print the values
    st.write('Value for i:', i_value)
    st.write('Value for j:', j_value)
else:
    st.write(f"Request failed with status code {response.status_code}")
    st.write("Response:")
    st.write(response.text)






def main():
    st.title("Vehicle Live Location on Map")

    m = folium.Map(location=[i_value, j_value], zoom_start=12)

    # Add marker for the input coordinates
    folium.Marker(
        location=[i_value, j_value],
        popup="Input coordinates",
        icon=folium.CustomIcon('https://worldofprintables.com/wp-content/uploads/2024/02/Free-Moving-Truck-SVG.svg', icon_size=(30, 30))
    ).add_to(m)

    # Find the bounds of the markers
    bounds = [[i_value, j_value], [i_value, j_value]]  # Initial bounds

    # Extend bounds to include the marker
    bounds[0][0] = min(bounds[0][0], i_value)
    bounds[0][1] = min(bounds[0][1], j_value)
    bounds[1][0] = max(bounds[1][0], i_value)
    bounds[1][1] = max(bounds[1][1], j_value)

    # Set the map's bounds
    m.fit_bounds(bounds)

    # Display the map
    folium_static(m)

if __name__ == "__main__":
    main()









#===============================================================================

url = 'https://www.vtapi.in:7820/vtapi/alarmHand/getAlarmInfoDetail'
headers = {
    'Token': token,
    'Content-Type': 'application/json',
    'lang': 'en_us'
}

data = {
    "vehicleIds": [vehicleid],
    "startTime": start_time_input,
    "endTime": end_time_input,
    "type": None,
    "alarmType": None,
    "alarmLevel": None,
    "alarmSource": None,
    "result": None,
    "pageNo": 1,
    "limitNum": 5000
}

response = requests.post(url, headers=headers, data=json.dumps(data))

data = response.json()
st.title("Active Safety Detail API Response ")
if start_time_input:
    alarm_detail = pd.DataFrame(data["data"])
    st.write(alarm_detail)
else:
    st.write("Enter Start and End Time")

    #st.write(len(alarm_detail))
selected_option = st.selectbox(f"Select a number from  0 to {len(alarm_detail)-1}", list(range(0, len(alarm_detail))))
json_data = json.dumps(data["data"][selected_option])
st.write(json_data)
json_data = json.loads(json_data)
alarm_sign = json_data['alarmSign']
pos_time = json_data['posTime']
vehicle_id = json_data['vehicleId']
st.write(alarm_sign,pos_time,vehicle_id)




def display_media(media_paths, media_type):
    num_media = len(media_paths)
    if num_media > 0:
        cols = st.columns(3)
        for i, link in enumerate(media_paths):
            col_idx = i % 3
            with cols[col_idx]:
                if media_type == 'video':
                    st.video(link)
                elif media_type == 'image':
                    st.image(link)

st.title('Active Safety Attachment Query Media')

url = 'http://43.204.169.66:7811/alarmHand/getAlarmAppendix'
headers = {
    'Token': token,
    'Content-Type': 'application/json',
    'lang': 'en_us'
}

vehicle_id = vehicle_id
pos_time = pos_time
alarm_sign = alarm_sign

if st.button('Submit'):
    if vehicle_id and pos_time and alarm_sign:
        try:
            data = {
                "vehicleId": vehicle_id,
                "posTime": pos_time,
                "alarmSign": alarm_sign
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_list = response.json().get('data', [])
                media_paths = [item['mediaPath'] for item in response_list]

                display_media([link for link in media_paths if link.endswith('.mp4')], 'video')
                display_media([link for link in media_paths if link.lower().endswith(('.jpg', '.jpeg'))], 'image')
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.warning('Please fill in all the fields.')





#================================================================================================================================
