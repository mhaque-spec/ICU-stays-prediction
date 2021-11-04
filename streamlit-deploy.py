import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('final-rForest.pkl')

PAGE_CONFIG = {"page_title":"ICU Prediction"}
st.set_page_config(**PAGE_CONFIG)

st.title('Predict how long your patient stays in the ICU!')

st.subheader('Basic Patient Information:')

age = st.slider('Age',0,100)
gender = st.selectbox('Select sex:',['F','M'])
weight = st.slider('Weight (kg)',0,300)
height = st.slider('Height (cm)',10,215)
religion = st.selectbox('Select belief system:',['CATHOLIC','JEWISH','PROTESTANT QUAKER','EPISCOPALIAN',
                                                 'GREEK ORTHODOX','CHRISTIAN SCIENTIST','BUDDHIST',"JEHOVAH'S WITNESS",
                                                 'UNITARIAN-UNIVERSALIST','BAPTIST','MUSLIM','ROMANIAN EAST. ORTH',
                                                 '7TH DAY ADVENTIST','HEBREW','METHODIST','HINDU','LUTHERAN',
                                                 'NOT SPECIFIED','OTHER' ,'PREFER NOT TO ANSWER'])

if religion == 'PREFER NOT TO ANSWER':
    religion = 'UNOBTAINABLE'

marital_status = st.selectbox('Select marital status:',['MARRIED','WIDOWED','SINGLE','DIVORCED','SEPARATED','UNKNOWN (DEFAULT)'])

ethnicity = st.selectbox('Select ethnicity:',['WHITE','UNKNOWN/NOT SPECIFIED','BLACK/AFRICAN AMERICAN','ASIAN',
                                              'HISPANIC OR LATINO','AMERICAN INDIAN/ALASKA NATIVE','ASIAN - CHINESE','ASIAN - VIETNAMESE',
                                              'BLACK/HAITIAN','BLACK/CAPE VERDEAN','NATIVE HAWAIIAN OR OTHER PACIFIC ISLAND','MULTI RACE ETHNICITY',
                                              'WHITE - RUSSIAN','HISPANIC/LATINO - PUERTO RICAN','OTHER','PATIENT DECLINED TO ANSWER','UNABLE TO OBTAIN'])

insurance = st.selectbox('Select insurance:',['MEDICARE','PRIVATE','MEDICARE-PRIVATE','MEDICAID','OTHER','FREE CARE','AUTO LIABILITY','SELF-PAY'])

st.subheader('Medical Information:')
sapsi = st.slider('SAPSI Score',1,40)
sofa = st.slider('SOFA Score',0,25)
care_unit = st.selectbox('Select care unit:',['MICU','CSRU','CCU','FICU','SICU','NICU'])
med_dur = st.slider('Medication duration (minutes)',0,40341974)
med_vol = st.slider('Medication volume (mL)',0,138713)
io_dur = st.slider('IV duration (minutes)',0,13246252)
diagnosis_word = st.slider('Critical diagnosis count',0,29)
cost_weight = st.slider('Calculated cost',0,20)

input_dic = {'gender':gender,'icustay_admit_age':age,'icustay_first_careunit':care_unit,'weight_first':weight,
             'sapsi_first':sapsi,'sofa_first':sofa,'cost_weight':cost_weight,'marital_status_descr':marital_status,
             'ethnicity_descr':ethnicity,'overall_payor_group_descr':insurance,'religion_descr':religion,'med_dur_min':med_dur,
             'total_amt':med_vol,'io_dur_min':io_dur,'diagnosis_count':diagnosis_word}
             
input_df = pd.DataFrame(columns=['gender', 'icustay_admit_age', 'icustay_first_careunit',
       'weight_first', 'sapsi_first', 'sofa_first', 'cost_weight',
       'marital_status_descr', 'ethnicity_descr', 'overall_payor_group_descr',
       'religion_descr', 'med_dur_min', 'total_amt', 'io_dur_min',
       'diagnosis_count'])
input_df = input_df.append(input_dic,ignore_index=True)

prediction = float(model.predict(input_df))
prediction = "{:.2f}".format(prediction)

if st.button('Predict!'):
    st.header(prediction + ' days')
