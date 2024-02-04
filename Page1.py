# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:22:57 2024

@author: Steve
"""

import streamlit as st
import numpy as np
import pandas as pd


if 'inputs' not in st.session_state:
    st.session_state['inputs']=[]
add=submit=None

if st.session_state['inputs']:
    st.write("### Your selections")
    temp=st.session_state['inputs'][0]
    for i in st.session_state['inputs'][1:]:
        temp=pd.concat([temp,i],axis=1)
    st.table(temp)
        
name=st.text_input('Please enter your name')
ftype=st.selectbox('Select Forest Type',[1,2,3,4,5],index=None)
state=st.selectbox('Select State',[1,2,3,4,5],index=None)
choice=st.selectbox('Select Inventory Data Type',['Age','Avg DBH and Height'],index=None)

if choice=='Age':
    l,r=st.columns(2)
    age=l.number_input('Enter the Age')
    acres=r.number_input('Enter the acres')
elif choice=='Avg DBH and Height':
    l2,m2,r2=st.columns(3)
    dbh=l2.number_input('Enter the dbh')
    height=m2.number_input('Enter the height')
    acres=r2.number_input('Enter the acres')
    
deferral=st.selectbox('Select the deferral period',list(range(0,125,5)),index=None)

if name and ftype and state and choice and deferral:
    l3,r3=st.columns(2)
    submit=l3.link_button('Submit',url='https://forest-carbon-tool-page2.streamlit.app/')
    add=r3.button('Add another forest type')
else:
    st.markdown('**:red[There are missing fields!]**')

if add:
    d={'Name':[],'Forest Type':[],'State':[],'Inventory Data Type':[],'Age':[],'Acres':[]
       ,'dbh':[],'height':[],'Deferral Period':[]}
    d['Name'].append(name)
    d['Forest Type'].append(ftype)
    d['State'].append(state)
    d['Inventory Data Type'].append(choice)
    if choice=='Age':
        d['Age'].append(age)
        d['Acres'].append(acres)
        d['dbh'].append('Not Selected')
        d['height'].append('Not Selected')
    elif choice=='Avg DBH and Height':
        d['Age'].append('Not Selected')
        d['Acres'].append(acres)
        d['dbh'].append(dbh)
        d['height'].append(height)
    d['Deferral Period'].append(deferral)
    d=pd.DataFrame(d)
    d=d.T
    d.columns=[f'Choice{len(st.session_state["inputs"])+1}']
    st.session_state['inputs'].append(d)
    st.rerun()

if submit:
    temp=st.session_state['inputs'][0]
    for i in st.session_state['inputs'][1:]:
        temp=pd.concat([temp,i],axis=1)
    temp.to_csv('temp.csv')
    


