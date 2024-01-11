# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:22:57 2024

@author: Steve
"""

import streamlit as st
import time
import mysql.connector
import pytz
from datetime import datetime

image1_url = '''
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1601922646204-b02a2ee287b3?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fHdoaXRlJTIwZm9yZXN0fGVufDB8fDB8fHww');
    background-size: cover;
    background-repeat: no-repeat;
    }
    </style>
    '''
st.markdown(image1_url, unsafe_allow_html=True)



st.markdown("""
            ## Forest Carbon and Market Decision Support Tool
            """)

#left, right = st.columns(2)
dbh = st.slider('Enter the dbh:',min_value=0,max_value=100)
price=st.slider('Enter the stumpage price:',min_value=0,max_value=100)
ag=st.slider('Enter the Annual Growth',min_value=0,max_value=100)

button=st.button('Calculate')


IST = pytz.timezone('America/Chicago')
now=datetime.now(IST)
now=now.strftime('%Y-%m-%d %H:%M:%S')

if button:
    formula=price*ag 
    
    if formula>2500:
        st.markdown(f"#### :green[Value is {formula}]")
    else:
        st.markdown(f"#### :red[Value is {formula}]")
        
    mydb = mysql.connector.connect(
        host="sql5.freemysqlhosting.net",
        user="sql5675822",
        password="Ks3GGjMHWD",
        database="sql5675822"
    )
    mycursor = mydb.cursor()
    mycursor.execute(f"insert into sample values ('{dbh}','{price}','{ag}','{formula}','{now}')")
    mydb.commit()
    mycursor.close()


