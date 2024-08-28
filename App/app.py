import pandas as pd
import streamlit as st
from helper import *

Summer , Winter = dataprocessor()
Summer , Winter = duplicates_row_removers(Summer,Winter)

Summer.dropna(subset=['region'],inplace=True)
Winter.dropna(subset=['region'],inplace=True)

st.sidebar.title('MENU')
season = st.sidebar.radio('Choose Season :',('Summer','Winter'))
options = st.sidebar.radio('Options :',('Medal-Tally','Country-Wise','Year-Wise','Year-Wise Progress'))

# .....MEDAL-TALLY.....

if season == 'Summer' and options == 'Medal-Tally':
    st.subheader('Summer Olympic Medals:')
    medal_pivot_summer = medal_tally_calculator(Summer)
    st.dataframe(medal_pivot_summer,width=700)

elif season == 'Winter' and options == 'Medal-Tally':
    st.subheader('Winter Olympic Medals:')
    medal_pivot_winter = medal_tally_calculator(Winter)
    st.dataframe(medal_pivot_winter,width=700)


elif season == 'Winter' and options == 'Country-Wise':
    st.subheader('Winter Country-Wise Olympic Medals:')
    medal_pivot_winter = medal_tally_calculator(Winter)
    NOC = st.selectbox('Selct NOC :',medal_pivot_winter.index)
    details = country_wise_search(NOC,medal_pivot_winter)
    table = pd.DataFrame.from_dict(details,orient='index',columns=['value'])
    st.dataframe(table)


elif season == 'Summer' and options == 'Country-Wise':
    st.subheader('Summer Country-Wise Olympic Medals:')
    medal_pivot_summer = medal_tally_calculator(Summer)
    NOC = st.selectbox('Selct NOC :',medal_pivot_summer.index)
    details = country_wise_search(NOC,medal_pivot_summer)
    table = pd.DataFrame.from_dict(details,orient='index',columns=['value'])
    st.dataframe(table)


elif season == 'Summer' and options == 'Year-Wise':
    st.subheader('Summer Olympic Year-Wise Medals:')
    years = sorted(Summer['Year'].unique())
    Selected_year = st.selectbox('Selct Year :',years)
    country = sorted(Summer[Summer['Year'] == Selected_year]['region'].unique())
    Selected_country = st.selectbox('Selct Year :',country)
    plot_medals(Selected_year,Selected_country,Summer)

elif season == 'Winter' and options == 'Year-Wise':
    st.subheader('Winter Olympic Year-Wise Medals:')
    years = sorted(Winter['Year'].unique())
    Selected_year = st.selectbox('Selct Year :',years)
    country = sorted(Winter[Winter['Year'] == Selected_year]['region'].unique())
    Selected_country = st.selectbox('Selct Year :',country)
    plot_medals(Selected_year,Selected_country,Winter)


elif season == 'Summer' and options == 'Year-Wise Progress':
    st.subheader('Summer Olympic Year-Wise Progress:')
    country = sorted(Summer['region'].unique())
    Selected_country = st.selectbox('Selct Year :',country)
    plot_year_progress(Selected_country,Summer)


elif season == 'Winter' and options == 'Year-Wise Progress':
    st.subheader('Winter Olympic Year-Wise Progress:')
    country = sorted(Winter['region'].unique())
    Selected_country = st.selectbox('Selct Year :',country)
    plot_year_progress(Selected_country,Winter)