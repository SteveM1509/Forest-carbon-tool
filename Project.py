# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:22:57 2024

@author: Steve
"""

import streamlit as st
import pandas as pd
from PIL import Image

def results(): # To display the selections and the equation images
    for i in st.session_state['selections']:
        right4.table(i)
    for i in st.session_state['equations']:
        im= Image.open(i+'.jpg')
        im=im.resize((400,600))
        equations4.image(im)

if 'selections' not in st.session_state: # Keep track of the selections of the user
    st.session_state['selections']=[]
if 'sub' not in st.session_state: # Keep track of the submit button
    st.session_state['sub']=False
if 'pf' not in st.session_state: # Keep track of whether present or future value is ongoing for future add another values
    st.session_state['pf']=False
if 'pf_click' not in st.session_state: # Keep track of whether pf has been clicked
    st.session_state['pf_click']=False
if 'add_another' not in st.session_state: # Keep track of whether add another has been clicked
    st.session_state['add_another']=False
if 'equations' not in st.session_state: # Keep track of the equations used for each calculation 
    st.session_state['equations']=[]
if 'cash_flow' not in st.session_state: # Keep track of what the user choice is
    st.session_state['cash_flow']=None

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
            
cf, sink, fc, fv = st.tabs(['Cash Flow','Sinking fund','Finanical Criterion','Forest Value'])

q1 = cf.selectbox("How often does the cash flow occur during the investment project or rotation length?",['Only Once','Every Year (Annual)',
                                                                                                         'Every nth year (Periodic)'],
                  index=None)

left, right = cf.columns(2)

q2 = right.number_input('Years revenue occurs',step=1)
q3=left.number_input('Enter the value')

left2, right2 = cf.columns(2)

q4=left2.number_input('Enter the rate of return (PERCENTAGE)', step=0.001)
if q4 and q4<1:
    pass
elif q4 and q4>=1:
    q4=q4/100

if q1=='Every nth year (Periodic)':
    q5=right2.number_input('Enter the period',step=1)

q6=cf.radio('Is it revenue or cost?',['Revenue','Cost'],index=None)

left3,right3=cf.columns(2)

q7=left3.number_input('Enter the Number of Years/Rotation',min_value=0, max_value=200, step=5)
right3.markdown("##### Note: Leave this blank if this is a perpetual cashflow")

left4, right4, equations4 = cf.columns(3)

results()

if q1 and q3 and q4 and (q1!='Every nth year (Periodic)' or q5) and q6 and not st.session_state['pf_click'] and not st.session_state['add_another'] and not st.session_state['sub']:
    if q7>q2 or q7==0:
        sub=left4.button('Submit')
        
        if st.session_state['pf']=='f' and q1 in ('Every Year (Annual)', 'Every nth year (Periodic)') and not q7 and sub:
            sub=False
            left4.markdown('**:red[Error! Cannot submit and calculate future value for a perpetual series]**')
        
    else:
        left4.markdown("""**:red['Number of years/rotation' must be 0 for present value or greater than 'Years revenue occurs' for future values]**""")

elif not st.session_state['sub'] and not st.session_state['pf_click'] and not st.session_state['add_another']:
    left4.markdown("""
                **:red[There are missing fields!]**
                """)

if sub:
    d={'Cash Flow':[q1],'Years Revenue':[q2],'Value':[q3],'Rate of Return':[q4],'Period':[q5],'Revenue/Cost':[q6],'Years/Rotation':[q7]}
    choice=len(st.session_state['selections'])+1
    st.session_state['selections'].append(pd.DataFrame(d, index=[f'Choice{choice}']).T)
    #st.markdown('**:green[Data submitted successfully!]**')
    st.session_state['sub']=True
    st.session_state['cash_flow']=q1
    st.rerun()
    
if st.session_state['sub']:
    if not st.session_state['pf']:
        if q7: # Providing both buttons if q7 is entered
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
        else:
            present = left4.button('Calculate Present Value')
            if present:
                st.session_state['pf']='p'
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
            

def calculate_result():
    # q3 = a, q4 = i, q7= years of rotation, q2= years revenue occurs
    a=q3
    i=q4
    t=q5
    n=None
    
    if (q1=='Every Year (Annual)' or q1=='Every nth year (Periodic)') and q7>0:
        n=q7
    elif st.session_state['pf']=='p':
        n=q2
    elif st.session_state['pf']=='f':
        n=q7-q2
    
    if q1=='Only Once':
        if st.session_state['pf']=='p':
            res = a/((1+i)**n)
        elif st.session_state['pf']=='f':
            res = a*((1+i)**n)
    
    elif q1=='Every Year (Annual)':
        
        if q7==0: # Goes forever
            
            if st.session_state['pf']=='p': # Only present value possible for this series
                res= a/i
        
        else: # Ends in n years
        
            if st.session_state['pf']=='p':
                num = ((1+i)**n)-1 
                den = i*((1+i)**n)
                res = a*num/den
            
            elif st.session_state['pf']=='f':
                
                res = a*(((1+i)**n)-1)/i
                
                
    elif q1=='Every nth year (Periodic)':
        
        if q7==0: # Goes forever
            
            if st.session_state['pf']=='p':
                res = a/(((i+1)**t)-1)
            
        else: # Ends in n years
            if st.session_state['pf']=='p':
                num = ((1+i)**n)-1
                den = (((1+i)**t)-1) * ((1+i)**n)
                res = a*num/den
                
            elif st.session_state['pf']=='f':
                num = ((1+i)**n)-1
                den = ((1+i)**t)-1
                res = a*num/den
    return round(res,2)
                
        
    
        
if st.session_state['pf_click']:
    
    res = calculate_result()
    val=None
    if st.session_state['pf']=='p':
        val = 'Present Value'
    elif st.session_state['pf']=='f':
        val = 'Future Value'
    
    temp = st.session_state['selections'][-1]
    temp.loc[val]=res
    st.session_state['pf_click']=False
    st.session_state['add_another']=True
    
    if st.session_state['cash_flow']=='Only Once':
        if val == 'Present Value':
            st.session_state['equations'].append('Only OncePresent Value')
        elif val == 'Future Value':
            st.session_state['equations'].append('Only OnceFuture Value')
            
    elif st.session_state['cash_flow']=='Every Year (Annual)':
        if not q7:
            st.session_state['equations'].append('Every Year (Annual)Present Value')
        else:
            if val == 'Present Value':
                st.session_state['equations'].append('Every Year (Annual)Present ValueTerminating')
            elif val == 'Future Value':
                st.session_state['equations'].append('Every Year (Annual)Future ValueTerminating')
                
    elif st.session_state['cash_flow']=='Every nth year (Periodic)':
        if not q7:
            st.session_state['equations'].append('Every nth year (Periodic)Present Value')
        else:
            if val == 'Present Value':
                st.session_state['equations'].append('Every nth year (Periodic)Present ValueTerminating')
            elif val == 'Future Value':
                st.session_state['equations'].append('Every nth year (Periodic)Future ValueTerminating')
            
        
        
    st.rerun()

if st.session_state['add_another']:
    
    aa=left4.button('Add Another')
    calc = left4.button('Calculate Net Value')
    if aa:
        #st.session_state['pf_click']=False
        #st.session_state['pf']=False
        st.session_state['add_another']=False
        st.rerun()
    
    if calc:
        s=0
        for i in st.session_state['selections']:
            if 'Present Value' in i.index:
                temp='Present Value'
            elif 'Future Value' in i.index:
                temp='Future Value'
                
            if i.loc['Revenue/Cost'][0]=='Revenue':
                s+=i.loc[temp][0]
            elif i.loc['Revenue/Cost'][0]=='Cost':
                s-=i.loc[temp][0]
        left4.markdown(f'#### :green[Net value is {round(s,2)}]')
            
    


    


    
    
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
