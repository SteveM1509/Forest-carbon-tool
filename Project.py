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

q1=q2=q3=button=None # Questions
p=i=n=t=a=v0=None # Parameters

st.markdown("""
            ## Forest Carbon and Market Decision Support Tool
            """)

st.markdown("""#### How often does the cash flow occur during the investment project or rotation length? """)

st.markdown("#### Is it only once (Single Sum)?")

q1 = st.radio('Choose an option',
              ['Yes','No'], index=None)

if q1=='Yes':
    v0=st.number_input('Enter the Present Value of single sum as a number',key='1')
    i=st.number_input('Enter the interest rate in percentage',key='2')
    n=st.number_input('Enter the number of interest bearing periods',key='3')
    if v0 and i and n:
        button=st.button('Calculate Future Value of Single Sum',key='4', type="primary")

elif q1=='No':
    st.markdown("#### Is it every year (Annual Series)?")
    
    q2= st.radio('Choose an option',
                  ['Yes','No'], index=None,key='5')
    
    if q2=='Yes':
        st.markdown("#### Does it go on forever or end after certain years?")
        q3=st.radio("Choose an option",['Goes on forever','Ends in n years'], index=None,key='6')
        
        if q3=='Goes on forever':
            a=st.number_input('Enter the equal annual payment',key='7')
            i=st.number_input('Enter the interest rate in percentage',key='8')
            if a and i:
                button=st.button('Calculate Present Value',key='9', type="primary")
        elif q3=='Ends in n years':
            a=st.number_input('Enter the equal annual payment',key='10')
            i=st.number_input('Enter the interest rate in percentage',key='11')
            n=st.number_input('Enter the number of interest bearing periods',key='12')
            if a and i and n:
                button=st.button('Calculate Present and Future Value of Single Sum',key='13', type="primary")
    elif q2=='No':
        st.markdown("#### So, it is periodic")
        st.markdown("#### Does it go on forever or end after certain years?")
        q3=st.radio("Choose an option",['Goes on forever','Ends in n years'], index=None,key='14')
        
        if q3=='Goes on forever':
            p=st.number_input('Enter equal periodic payment',key='15')
            i=st.number_input('Enter the interest rate in percentage',key='16')
            t=st.number_input('Enter the interval between periodic payment',key='17')
            if p and i and t:
                button=st.button('Calculate Present Value',key='18', type="primary")
        elif q3=='Ends in n years':
            p=st.number_input('Enter equal periodic payment',key='19')
            i=st.number_input('Enter the interest rate in percentage',key='20')
            t=st.number_input('Enter the interval between periodic payment',key='21')
            n=st.number_input('Enter the number of interest bearing periods',key='22')
            if p and i and n and t:
                button=st.button('Calculate Present and Future Value',key='23', type="primary")

IST = pytz.timezone('America/Chicago')
now=datetime.now(IST)
now=now.strftime('%Y-%m-%d %H:%M:%S')

if button:
    if (q1,q2,q3)==('Yes',None,None):
        vn=v0*((1+i)**n)
    
    elif (q1,q2,q3)==('No','Yes','Goes on forever'):
        v0=a/i
    
    elif (q1,q2,q3)==('No','Yes','Ends in n years'):
        num=a*(((1+i)**n)-1)
        den=i*((1+i)**n)
        v0=num/den
        vn=num/i
    
    elif (q1,q2,q3)==('No','No','Goes on forever'):
        v0=p/(((1+i)**t)-1)
    
    elif (q1,q2,q3)==('No','No','Ends in n years'):
        num=p*(((1+i)**n)-1)
        den=(((1+i)**t)-1)*((1+i)**n)
        v0=num/den
        vn=num/(((1+i)**t)-1)
    
    if vn and v0:
        st.markdown(f'#### :green[The present value is {round(v0,2)} and the future value is {round(vn,2)}]')
    elif vn:
        st.markdown(f'#### :green[The future value is {round(vn,2)}]')
    elif v0:
        st.markdown(f'#### :green[The present value is {round(v0,2)}]')
    
    
    # mydb = mysql.connector.connect(
    #     host="sql5.freemysqlhosting.net",
    #     user="sql5675822",
    #     password="Ks3GGjMHWD",
    #     database="sql5675822"
    # )
    # mycursor = mydb.cursor()
    # mycursor.execute(f"insert into sample values ('{dbh}','{price}','{ag}','{formula}','{now}')")
    # mydb.commit()
    # mycursor.close()
