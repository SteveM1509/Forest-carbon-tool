# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:22:57 2024

@author: Steve
"""

import streamlit as st
import pandas as pd

def results():
    for i in st.session_state['selections']:
        right4.table(i)

if 'selections' not in st.session_state:
    st.session_state['selections']=[]
if 'sub' not in st.session_state:
    st.session_state['sub']=False
if 'pf' not in st.session_state:
    st.session_state['pf']=False
if 'pf_click' not in st.session_state:
    st.session_state['pf_click']=False

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

q1=q2=q3=q4=q5=q6=q7=sub=present=future=None

st.markdown("""
            ## Forest Economics and Decision Support
            """)
            
cf, fc, fv = st.tabs(['Cash Flow','Finanical Criterion','Forest Value'])

q1 = cf.selectbox("How often does the cash flow occur during the investment project or rotation length?",['Only Once','Every Year (Annual)',
                                                                                                         'Every nth year (Periodic)'],
                  index=None)

left, right = cf.columns(2)

q2 = left.number_input('Years revenue occurs',step=1)
q3=right.number_input('Enter the value', step=1)

left2, right2 = cf.columns(2)

q4=left2.number_input('Enter the rate of return (PERCENTAGE)', step=1)

if q1=='Every nth year (Periodic)':
    q5=right2.number_input('Enter the period',step=1)

q6=cf.radio('Is it revenue or cost?',['Revenue','Cost'],index=None)

left3,right3=cf.columns(2)

q7=left3.number_input('Enter the Number of Years/Rotation',min_value=0, max_value=200, step=5)
right3.markdown("##### Note: Leave this blank if this is a perpetual cashflow")

left4, right4 = cf.columns(2)

results()

if q1 and q2 and q3 and q4 and (q1!='Every nth year (Periodic)' or q5) and q6 and q7:
    sub=left4.button('Submit')

if sub:
    d={'Cash Flow':[q1],'Years Revenue':[q2],'Value':[q3],'Rate of Return':[q4],'Period':[q5],'Revenue/Cost':[q6],'Years/Rotation':[q7]}
    choice=len(st.session_state['selections'])+1
    st.session_state['selections'].append(pd.DataFrame(d, index=[f'Choice{choice}']).T)
    #st.markdown('**:green[Data submitted successfully!]**')
    st.session_state['sub']=True
    st.rerun()
    
if st.session_state['sub']:
    if not st.session_state['pf']:
        present = left4.button('Calculate Present Value')
        future = left4.button('Calculate Future Value')
        if present:
            st.session_state['pf']='p'
            st.session_state['pf_click']=True
            st.session_state['sub']=False
            
            st.rerun()
            
        elif future:
            st.session_state['pf']='f'
            st.session_state['pf_click']=True
            st.session_state['sub']=False
            
            st.rerun()
    
    elif st.session_state['pf']=='p':
        present = left4.button('Calculate Present Value')
        if present:
            st.session_state['pf']='p'
            st.session_state['pf_click']=True
            st.session_state['sub']=False
            
            st.rerun()
    
    elif st.session_state['pf']=='f':
        future = left4.button('Calculate Future Value')
        if future:
            st.session_state['pf']='f'
            st.session_state['pf_click']=True
            st.session_state['sub']=False
            
            st.rerun()
        
    
        
if st.session_state['pf_click']:
    # do some calculations and append the result to the dataframe
    #st.rerun()
    aa=left4.button('Add Another')
    if aa:
        st.session_state['pf_click']=False
        #st.session_state['pf']=False
        st.rerun()
    


    


    
    
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
