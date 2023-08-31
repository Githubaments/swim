import streamlit as st
import pandas as pd
import plotly.express as px


def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h*3600 + m*60 + s

def seconds_to_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"


# Title
st.title("Swimming Analysis Dashboard")

# Upload CSV data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
    
    # Convert time columns to total seconds
    data['Handicap_seconds'] = data['Handicap'].apply(time_to_seconds)
    data['Race Time_seconds'] = data['Race Time'].apply(time_to_seconds)
    data['Swim Time_seconds'] = data['Swim Time'].apply(time_to_seconds)



    
    # Convert Distance to numeric if needed
    if data['Distance'].dtype == 'O':  # If Distance is an object (string)
        data['Distance'] = data['Distance'].str.replace(',', '').str.replace('m', '').astype(int)

    # Multi-select swimmer from the data
    selected_swimmers = st.multiselect("Select swimmers:", data['Name'].unique())

    if selected_swimmers:
        # Filter data for the selected swimmers
        filtered_data = data[data['Name'].isin(selected_swimmers)]

        # Handicap Over Time with Distance as point size
        fig1 = px.scatter(filtered_data, x='Date', y='Handicap', size='Distance', color='Name', title='Handicap Over Time')
        st.plotly_chart(fig1)

        # Race Time Over Time with Distance as point size
        fig2 = px.scatter(filtered_data, x='Date', y='Swim Time', size='Distance', color='Name', title='Swim Time Over Time')
        st.plotly_chart(fig2)

        # Pace/100m Over Time with Distance as point size
        fig3 = px.scatter(filtered_data, x='Date', y='Pace/100m', size='Distance', color='Name', title='Pace/100m Over Time')
        st.plotly_chart(fig3)
    else:
        st.write("Please select swimmers to visualize their performance.")
else:
    st.write("Please upload your summary CSV file.")
