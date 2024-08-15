#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# In[2]:


# Firebase setup
st.title("Firebase Firestore Data Visualization")


# In[ ]:





# In[3]:



# Initialize Firebase
@st.cache_resource
def initialize_firebase():
    cred = credentials.Certificate({
        # Your Firebase credentials here
  "type": "service_account",
  "project_id": "doyenifypanelapi",
  "private_key_id": "da19d7aed2a5591a996b50da828a12398ca52ae1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCrKK0x/uUFaWLh\nnGoj0svLaIeouCrf8uH5l6cw0wb6aRcKRAbOV3Onc2viEPK0vbbBQB7lo+s1Vxes\nPuQvvWsv6SKCieknX6/heKAkW6Gq7ZSQRGZ61+x4rvSknwTvfSo6n+Yt2QqiW9DL\n8e+YUrmqLoucuFKOaSAV6uogc1SMxLWtOZaDMUUW7SJF2CrVXc1BJ38JfjgEZyX1\nvMKxf81uQMLmxm0sbuUGENfu07hJ8Q5xUwEWXaGbzpJLlXux/BSDijKlSqlolGCH\nRp/L/MIM7soxx70gVcHTWJzBQ+F0Z3Afd6Zv8AS6TXJDF7NDLFESojmSC8dfVwxb\nWJOrBCWDAgMBAAECggEAR5IUTkYsZUVqtDWwSneQgWed5obQYuIQ7UolfuyXS+na\n2Q+WGv2Fnp1MnPUCUGLOQ2P5J4SSS7U18HBCAdZ+tkOSCyz5Al5oUOucZ2erpCqB\nh4waoD6fIt3h7d6S9UQM/wOzADP0Vuz20/lAe50IByo8dhW7a9J4uMGJEnW3gr7l\nsEesZu5iF2APp9j030riB2/TNFEund1tYfuAmrdyJEdq4wiie+Cv5SmSQFjZCBwh\nQeUvANygZeThhbjZXJTy3VEkytqDfaX4V+Yae0uTbdTH/tLxJMTzKnoZ2K4MoVeq\nb0S3esNv7spGV9gQSktXj1SRg5Y1lf0LgpfBXesLUQKBgQDWERqzXzga88fvKBk/\nHJvti6Nm8sGPyTnThBVB18otenM74D0WkByRTFS5p5fkm50wmTjk4se0HMl2FXZH\njg9lZKLLhuXqrInFIbGMOmELf1ki7nkr6ADObI5RGlvEjBuhi2x04lcWlmBpP1xx\n8izvwBW4Me6uQ3dE/nl/igAUkwKBgQDMr9nr9Twl2Nwq05F8d2bOEIgqamMB0OXk\n9klUncFLMJs3klPfNQHgD2ILGdGkkAunMioMOiDQr8tOOsxsQ9BKfcMuFFDajVa8\nZG8OueSgVvs66gfNAP3iNrrvXUcYPzr2KeT9Mt0mTKv3LQIFSf6vgmxJss63YqFe\nNWMOYKyxUQKBgQDNtiQliXR+GhThE3SnfJOvhEgjj1dJGMPUKpLO8lLcv1ZrjMLH\noveA/YxR2OcTjiNRZ30QH4pv4FYNfvRqMO9ErZ/v3BOoH+RJJ2babeOCS//ZnLee\n5NWZiSJ+d8kGKOoIpNY1wKiWES5XFcd9zI84WivFFV7b4gOErtMNKA2JtwKBgDKQ\npqcx2AAJiKpTxbcX0B/L2beQvJCwSHq9lPQAXMX0ZgPedDXJ5IKziibv4+hhZV+S\nduy6V2z2YKUcxW9heU1NsC/r+OVk0S6NKRpcNeyeUEYHlpHAUvfVSWzkgDGvPSOe\nyeD69cMGYd0YE023L+GvuIykTYjkJrUdPzFIFKFhAoGBALNzpE6AzHlYD2uVuAZo\nd8vet/fGcc9TdlwthB33DBKvjNLch9YKBtAnddLgMgJfw7b19s9aKwqitdTSLPkF\nGDejujwBBHcNMrOYO/H1HLgetNJOqpBOjZCvSqsP5B0dd9UBU0JkZeJx7RLX6S7J\nePWybSMilHdF+kOK4A5XX0a9\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-8sy6x@doyenifypanelapi.iam.gserviceaccount.com",
  "client_id": "101420797003633405852",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8sy6x%40doyenifypanelapi.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
    })
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_firebase()

@st.cache_data
def load_data():
    course_registration_ref = db.collection('CourseRegistration')
    docs = course_registration_ref.stream()
    data = [doc.to_dict() for doc in docs]
    df = pd.DataFrame(data)
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df['Date'] = df['createdAt'].dt.date
    df['Time'] = df['createdAt'].dt.time
    return df

def convert_price_to_euro(df, currency_symbol):
    df['TotalpaidinEURO'] = df.apply(
        lambda row: row['paidPrice'] if row['paymentCurrency'] == currency_symbol else 0,
        axis=1
    )
    df['TotalpaidinNAIRA'] = df.apply(
        lambda row: row['paidPrice'] if row['paymentCurrency'] != currency_symbol else 0,
        axis=1
    )
    return df

# Load and preprocess data
df = load_data()
df = convert_price_to_euro(df, currency_symbol='€')

# Streamlit app
st.title("DOYEN DASH")

# Sidebar for cohort selection
selected_cohort = st.sidebar.selectbox(
    "Select Cohort",
    options=df['cohort'].unique(),
    format_func=lambda x: f"Cohort {x}"
)

# Filter data based on selected cohort
filtered_df = df[df['cohort'] == selected_cohort]

# Stacked bar chart
st.header(f"Source of Discovery for Cohort {selected_cohort}")
count_source_of_discovery = filtered_df.groupby(['course', 'sourceOfDiscovery']).size().reset_index(name='count')
fig_bar = px.bar(
    count_source_of_discovery,
    x='course',
    y='count',
    color='sourceOfDiscovery',
    title=f'Source of Discovery for Cohort {selected_cohort}',
    labels={'count': 'Count', 'course': 'Course'},
    barmode='stack'
)
st.plotly_chart(fig_bar)

# Table for total paid in EURO & NAIRA
st.header("Total Paid in EURO & NAIRA by Course and Cohort")
total_amount_in_courses = filtered_df.groupby('course')[['TotalpaidinEURO', 'TotalpaidinNAIRA']].sum().reset_index()
st.dataframe(total_amount_in_courses)

# Table for course application count by cohort
st.header("Count of Course Applications by Cohort")
no_of_courses = filtered_df.groupby(['cohort', 'course']).size().reset_index(name='count')
st.dataframe(no_of_courses)

# Pie chart and table for general cohort distribution
st.header("General Cohort Distribution")

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "domain"}, {"type": "table"}]],
    subplot_titles=("Location Distribution", "Course Registration Status")
)

# Pie chart
pie_chart_data = df['userIp'].value_counts().reset_index(name='count')
pie_chart_data.columns = ['userIp', 'count']
fig.add_trace(go.Pie(labels=pie_chart_data['userIp'], values=pie_chart_data['count'], hole=0.3), row=1, col=1)

# Table
count_per_course_status = df.groupby(['course', 'status']).size().reset_index(name='count')
fig.add_trace(go.Table(
    header=dict(values=['Course', 'Status', 'Count'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[count_per_course_status.course, count_per_course_status.status, count_per_course_status['count']],
               fill_color='lavender',
               align='left')
), row=1, col=2)

fig.update_layout(height=600, width=1000)
st.plotly_chart(fig)

# Additional statistics
st.header("Additional Statistics")
st.write("Total Amount In Category of Courses:")
TotalAmount_In_Categoryofcourses = df.groupby("course")["TotalpaidinEURO"].sum()
st.write(TotalAmount_In_Categoryofcourses)

st.write("Count of Source of Discovery:")
Count_SourceofDis = df['sourceOfDiscovery'].value_counts()
st.write(Count_SourceofDis)

# You can add more visualizations or statistics as needed


# In[ ]:




