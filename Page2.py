# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 18:42:48 2024

@author: Steve
"""

import streamlit as st
import numpy as np
import pandas as pd


submit=None


sell = st.selectbox('If you were to sell timber today, who would buy it?',['Sawmill','Pulp','Biomass','None',"I don't know"],index=None)
hard,soft = st.columns(2)

hard.markdown("### Hardwood")
soft.markdown("### Softwood")

hard_log = hard.number_input('Enter the log price',key=1)
hard_x = hard.number_input('Enter the x price',key=2)
hard_biomass = hard.number_input('Enter the biomass price',key=3)
hard_stump = hard.number_input('What is the stumpage price',key=4)

soft_log = soft.number_input('Enter the log price')
soft_x = soft.number_input('Enter the x price')
soft_biomass = soft.number_input('Enter the biomass price')
soft_stump = soft.number_input('What is the stumpage price')

roi = st.number_input('Minimum acceptable rate of return in percentage')
ep = st.number_input('Expected price of carbon credit')

if sell and roi and ep:
    submit = st.button('Submit')
else:
    st.markdown('**:red[There are missing fields!]**')

if submit:
    st.markdown('Your selections')
    d={'Buyer':[sell],'Harddwood log price':[hard_log],'Hardwood x price':[hard_x],'Hardwood biomass':[hard_biomass],'Hardwood stumpage price':[hard_stump],
       'Softwood log price':[soft_log],'Softwood x price':[soft_x],'Softwood biomass price':[soft_biomass],'Softwood stumpage price':[soft_stump],
       'ROI':[roi],'Expected price':[ep]}
    d=pd.DataFrame(d)
    st.table(d.T)
