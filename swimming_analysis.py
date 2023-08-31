import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Swimming Analysis Dashboard")

# Upload CSV data
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
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
