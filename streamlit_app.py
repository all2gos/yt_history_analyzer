import pandas as pd
import os,json
import streamlit as st

pd.options.mode.chained_assignment = None
st.title('LSowa analiza')

"""
## Dzieeeeeeeeeń dobry

Stworzyłem tą aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON z historią oglądania](https://www.youtube.com/watch?v=zlzzO1e6dws)
"""
df = pd.DataFrame()
file = st.file_uploader("Tutaj wklej swoją historię")
lsmode = st.button('Usuń wszystkie filmy poza LSowymi')
st.button()
if file is not None:
    df = pd.read_json(file)     
    df = df.drop(['products','activityControls','description','details'], axis = 1)
    len_1 = len(df)
    df = df.dropna()
    len_2 = len(df)
    df['hour'] = df['time']
    df['day_of_week'] = pd.DatetimeIndex(df['time']).day_of_week
    df['year'] = pd.DatetimeIndex(df['time']).year
    df['month'] = pd.DatetimeIndex(df['time']).month
    df['year_month'] = df['time']
    df['wideo'] = df['time']    

    st.write('W wyniku usuwania uszkodzonych informacji,', len_1-len_2, 'pozycji z historii zostało usuniętych')
    st.write('Konwertowanie pliku JSON trwa. Proszę o cierpliwość ten proces może trwać 2-3 minuty')

    for item in range(len(df)):
        df['subtitles'].iloc[item] = df['subtitles'].iloc[item][0]['name']
        df['hour'].iloc[item] = df['time'].iloc[item][11:13]
        df['year_month'].iloc[item] = df['time'].iloc[item][:7]
        df['time'].iloc[item] = df['time'].iloc[item][:10]
        df['wideo'].iloc[item] = df['title'].iloc[item][10:]        
       
    st.write('Najczęściej oglądane wideo')
    st.write(df['wideo'].value_counts())
    st.write('Najczęściej oglądane kanały')
    st.write(df['subtitles'].value_counts())


    st.write('Dane dla LSa')
    df = df[df['subtitles']=='Lekko Stronniczy']
    st.write('Najczęściej oglądany LS')
    st.write(df['wideo'].value_counts())
    





