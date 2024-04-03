# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 15:22:57 2024

@author: Steve
"""
# Make picture smaller. Option to show/unshow pictures
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

def results(): # To display the selections and the equation images
    if len(st.session_state['selections']):
        selections=st.session_state['selections'][0]
    
    for i in st.session_state['selections'][1:]:
        selections=pd.concat([selections,i],axis=1)
    
    if len(st.session_state['selections']):
        bottom_most.table(selections)
    
    equations = pd.Series(st.session_state['equations'])
    equations = equations.unique()
    
    if len(equations):
        im_check = bottom_most2.checkbox('Show equations used')
    final_im = Image.new('RGB',(100*len(equations),150))
    for i in range(len(equations)):
        im= Image.open(equations[i]+'.jpg')
        im=im.resize((100,150))
        final_im.paste(im,((i*100),0))
    if len(equations) and im_check:
        bottom_most2.image(final_im)

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
if 'calc' not in st.session_state:
    st.session_state['calc']=None
if 'q4' not in st.session_state:
    st.session_state['q4']=False


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

def calculate_result(q1_temp,q2_temp,q3_temp,q4_temp,q5_temp,q7_temp):
    # q3 = a, q4 = i, q7= years of rotation, q2= years revenue occurs
    if q1_temp == 'Annual':
        q1_temp = 'Every Year (Annual)'
    elif q1_temp == 'Periodic':
        q1_temp = 'Every nth year (Periodic)'
    if q7_temp=='\u221e':
        q7_temp=0
    a=q3_temp
    i=q4_temp
    t=q5_temp
    n=None
    
    if (q1_temp=='Every Year (Annual)' or q1_temp=='Every nth year (Periodic)') and q7_temp>0:
        n=q7_temp
    elif st.session_state['pf']=='p':
        n=q2_temp
    elif st.session_state['pf']=='f':
        n=q7_temp-q2_temp
    
    if q1_temp=='Only Once':
        if st.session_state['pf']=='p':
            res = a/((1+i)**n)
        elif st.session_state['pf']=='f':
            res = a*((1+i)**n)
    
    elif q1_temp=='Every Year (Annual)':
        
        if q7_temp==0: # Goes forever
            
            if st.session_state['pf']=='p': # Only present value possible for this series
                res= a/i
        
        else: # Ends in n years
        
            if st.session_state['pf']=='p':
                num = ((1+i)**n)-1 
                den = i*((1+i)**n)
                res = a*num/den
            
            elif st.session_state['pf']=='f':
                
                res = a*(((1+i)**n)-1)/i
                
                
    elif q1_temp=='Every nth year (Periodic)':
        
        if q7_temp==0: # Goes forever
            
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

q1=q2=q3=q4=q5=q6=q7=sub=present=future=delete=None

st.markdown("""
            ## Forest Economics and Decision Support
            """)
            
cf, sink, fv = st.tabs(['Finanical Criterion','Sinking fund','Forest Value'])

q1 = cf.selectbox("How often does the cash flow occur during the investment project or rotation length?",['Only Once','Every Year (Annual)',
                                                                                                         'Every nth year (Periodic)'],
                  index=None)

left, right = cf.columns(2)

if q1 != 'Every nth year (Periodic)':
    if q1=='Every Year (Annual)':
        q2 = right.number_input('First year revenue occurs',step=1,value=1,disabled=True)
    else:
        q2 = right.number_input('Years revenue occurs',step=1)
q3=left.number_input('Enter the value')

left2, right2 = cf.columns(2)

if q1=='Every nth year (Periodic)':
    q5=right.number_input('Enter the period',step=1)

q6=cf.radio('Is it revenue or cost?',['Revenue','Cost'],index=None)

left3,right3=cf.columns(2)

q7=left3.number_input('Enter the Number of Years/Rotation',min_value=0, max_value=200, step=5)
right3.markdown("##### Note: Leave this blank if this is a perpetual cashflow")

left4, right4 = cf.columns(2)
bottom_most,_ = cf.columns([0.99,0.01])
bottom_most2,_=cf.columns([0.99,0.01])
choices = [i.columns[0] for i in st.session_state['selections']]
delete_choice = left4.selectbox('Delete a choice', choices, index=None)
if delete_choice:
    right4.markdown('\n\n')
    right4.markdown('\n\n')
    delete = right4.button('Delete',type="primary")
if delete:
    temp = int(delete_choice[-1])
    temp=temp-1
    st.session_state['selections'].pop(temp)
    st.session_state['equations'].pop(temp)
    for i in range(len(st.session_state['selections'])):
        st.session_state['selections'][i].columns=[f'Choice{i+1}']
    
    st.rerun()    

results()

condition1 = q1 and q3 and q6 # Basics required for all things
condition2 = not st.session_state['pf_click'] and not st.session_state['add_another'] and not st.session_state['sub'] # Don't display while they are in a add another or another step for easy process flow
condition3 = q1!='Every nth year (Periodic)' or q5 # If periodic q5 is mandatory else fine
condition4 = q1!='Only Once' or q2>0

if condition1 and condition2 and condition3 and condition4:
    if q1 == 'Only Once' or q7==0 or (q1 == 'Every nth year (Periodic)' and q7>q5) or (q1 == 'Every Year (Annual)' and q7>q2) : # If q1 is single sum, ignore everything. Else, next check if it is terminating. Next if periodic, make sure that q7 is the highest. Finally, if it is annual series, make sure q7 is greater than q2
        if st.session_state['pf']:
            text = 'Add Another'
        else:
            text='Submit'
        sub=left4.button(text)
        
        if sub:
            st.session_state['calc']=False
            st.session_state['q4']=False
        
        if st.session_state['pf']=='f' and q1 in ('Every Year (Annual)', 'Every nth year (Periodic)') and not q7 and sub:
            sub=False
            left4.markdown('**:red[Error! Cannot submit and calculate future value for a perpetual series]**')
            
        if st.session_state['pf']:
            right4.markdown('\n')
            right4.markdown('\n')
            right4.markdown('\n')
            right4.markdown('\n')
            right4.markdown('\n')
            right4.markdown('\n')
            calc = right4.button('Calculate Net Value and other criterion')
            
            if calc:
                st.session_state['calc']=True
        
    else:
        left4.markdown("""**:red['Number of years/rotation' must be 0 for present value or greater than 'Years revenue occurs' for future values]**""")

elif condition2:
    left4.markdown("""
                **:red[There are missing fields!]**
                """)

if st.session_state['calc']:
    q4=right4.number_input('Enter the rate of return (PERCENTAGE)', step=0.001)
    if q4 and q4<1:
        pass
    elif q4 and q4>=1:
        q4=q4/100
        
    q4_confirm = right4.button('Confirm')
    
    if q4_confirm:
        for i in st.session_state['selections']:
            val=None
            if st.session_state['pf']=='p':
                val = 'Present Value'
            elif st.session_state['pf']=='f':
                val = 'Future Value'
            
            res = calculate_result(i.loc['Cash Flow'][0],i.loc['Years Revenue'][0],i.loc['Value'][0],q4, i.loc['Period'][0],i.loc['Years/Rotation'][0])
            i.loc[val]= res
        st.session_state['q4']=True
        st.rerun()
        
if st.session_state['q4']:
    s=0 
    costs=0
    benefits=0
    for i in st.session_state['selections']:
        if 'Present Value' in i.index:
            temp='Present Value'
        elif 'Future Value' in i.index:
            temp='Future Value'
            
        if i.loc['Revenue/Cost'][0]=='Revenue':
            s+=i.loc[temp][0]
            benefits+=i.loc[temp][0]
        elif i.loc['Revenue/Cost'][0]=='Cost':
            s-=i.loc[temp][0]
            costs+=i.loc[temp][0]
    
    if costs:
        bc_ratio = round(benefits/costs,3)
    else:
        bc_ratio = '\u221e'
    if s>0:
        left4.markdown(f'#### :green[Net {temp.split(" ")[0]} value is {round(s,2)}]')
        temp = 'increasing'
    elif s<=0:
        left4.markdown(f'#### :red[Net {temp.split(" ")[0]} Value is {round(s,2)}]')
        temp = 'decreasing'
    if not costs or bc_ratio>=1:
        left4.markdown(f'#### :green[Benefit to Cost ratio is {bc_ratio}]')
    elif costs and bc_ratio<1:
        left4.markdown(f'#### :red[Benefit to Cost ratio is {bc_ratio}]')
        
    res=0
    irr=0
    power=1
    
    if temp=='increasing':
        ran_min = 0.01 
        ran_max = 1 
        ran = np.arange(ran_min,ran_max,0.1**power)
    elif temp=='decreasing':
        ran_min = 1
        ran_max = 0.01 
        ran = np.arange(ran_min,ran_max,-(0.1**power))
    

    while min(ran)>0.001:
        if temp=='increasing':
            ran = np.arange(ran_min,ran_max,0.1**power)
        elif temp=='decreasing':
            ran = np.arange(ran_min,ran_max,-(0.1**power))
        res_list=[]
        
        if len(ran)>30:
            print('Something went wrong!!!')
            break
        
        for j in range(len(ran)):
            for i in st.session_state['selections']:
                res = calculate_result(i.loc['Cash Flow'][0],i.loc['Years Revenue'][0],i.loc['Value'][0],ran[j], i.loc['Period'][0],i.loc['Years/Rotation'][0])
            res_list.append(res)
            if res<0:
                if temp=='increasing':
                    irr+=ran[j-1]
                    ran_min=ran[j]
                    ran_max=ran[j-1]
                elif temp=='decreasing':
                    irr+=ran[j]
                    ran_min=ran[j-1]
                    ran_max=ran[j]
                break  
        power+=1
    if irr:
        left4.markdown(f'#### The IRR value is {irr}')
    else:
        left4.markdown('#### The IRR does not exist')
        
    lev_df = st.session_state['selections'][-1]
    lev_q1 = lev_df.loc['Cash Flow'][0]
    lev_q2 = lev_df.loc['Years Revenue'][0]
    lev_q7 = lev_df.loc['Years/Rotation'][0]
    if (lev_q1=='Annual' or lev_q1=='Periodic') and lev_q7>0:
        lev_n=lev_q7
    elif st.session_state['pf']=='p':
        lev_n=lev_q2
    elif st.session_state['pf']=='f':
        lev_n=lev_q7-lev_q2
        
    if st.session_state['pf']=='p':
        aei = s * (q4*((q4+1)**lev_n))/(((q4+1)**lev_n)-1)
        lev = (s/(((1+q4)**lev_n)-1))+s
    elif st.session_state['pf']=='f':
        aei = s*q4/(((q4+1)**lev_n)-1)
        lev = s/(((1+q4)**lev_n)-1)
    
    if aei and lev:
        left4.markdown(f'#### The LEV is {round(lev,2)}')
        left4.markdown(f'#### The AEI is {round(aei,2)}')
    
    

if sub:
    if not q7 and q1 in ['Every Year (Annual)','Every nth year (Periodic)']:
        q7='\u221e'
    if q1=='Every nth year (Periodic)':
        q1_temp='Periodic'
    elif q1=='Every Year (Annual)':
        q1_temp = 'Annual'
    else:
        q1_temp=q1
    d={'Cash Flow':[q1_temp],'Years Revenue':[q2],'Value':[q3],'Period':[q5],'Revenue/Cost':[q6],'Years/Rotation':[q7]}
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
        st.session_state['pf']='p'
        st.session_state['pf_click']=True
        st.session_state['sub']=False
        
        st.rerun()
    
    elif st.session_state['pf']=='f':
        st.session_state['pf']='f'
        st.session_state['pf_click']=True
        st.session_state['sub']=False
        
        st.rerun()
                
if st.session_state['pf_click']:
    
    #res = calculate_result()
    val=None
    if st.session_state['pf']=='p':
        val = 'Present Value'
    elif st.session_state['pf']=='f':
        val = 'Future Value'
    
    # temp = st.session_state['selections'][-1]
    # temp.loc[val]=res
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
    
    aa=True
    if aa:
        #st.session_state['pf_click']=False
        #st.session_state['pf']=False
        st.session_state['add_another']=False
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


