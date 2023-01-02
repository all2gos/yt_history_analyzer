import pandas as pd
import streamlit as st
import datetime
import numpy as np


pd.options.mode.chained_assignment = None
st.title('LSowa analiza')

"""
## Dzieeeeeeeeeń dobry

Stworzyłem tę aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON z historią oglądania](https://webapps.stackexchange.com/questions/101263/how-can-i-export-youtubes-personal-history)

"""
def data_preprocessing(file):
    df = pd.read_json(file)
    #df = df.drop(['products','activityControls','description','details'], axis = 1)
     
    
    df['hour'] = df['time']
    df['day_of_week'] = pd.DatetimeIndex(df['time']).day_of_week
    df['year'] = pd.DatetimeIndex(df['time']).year
    df['month'] = pd.DatetimeIndex(df['time']).month
    df['year_month'] = df['time']
    df['wideo'] = df['time']    
    df['channel'] = df['subtitles']
    st.write('Konwertowanie pliku JSON trwa. Proszę o cierpliwość ten proces może trwać 2-3 minuty')   
    list_of_nan = []
    for item in range(len(df)):
        try:
            df['channel'].iloc[item] = df['channel'].iloc[item][0]['name']
        except:
            list_of_nan.append(item)
        df['hour'].iloc[item] = df['time'].iloc[item][11:13]
        df['year_month'].iloc[item] = df['time'].iloc[item][:7]
        df['time'].iloc[item] = df['time'].iloc[item][:10]
        df['wideo'].iloc[item] = df['title'].iloc[item][10:]   
        df['time'].iloc[item] = datetime.date(int(df['time'].iloc[item][:4]),int(df['time'].iloc[item][5:7]),int(df['time'].iloc[item][8:])) 
    st.write('W wyniku usuwania uszkodzonych informacji,', len(list_of_nan), 'pozycji z historii zostało usuniętych')
    return df, len(df)

file = st.file_uploader("Tutaj wklej swoją historię")
channel = st.text_input('','Wybierz kanał, którego statystyki oglądania chcesz wyświetlić, nie wpisując nic wybierasz wszystkie')
st.write('Jeżeli wpiszesz kanał, który nie występuje w Twojej historii wówczas statystyki dalej będą wyświetalne dla wszystkich kanałów')
st.write('Wybierz jakie statystyki chcesz zobaczyć')

top_video = st.checkbox('Najczęściej oglądane filmy')

st.write('Liczbę filmów zobaczonych w danym:')
year = st.checkbox('roku')
year_month = st.checkbox('miesiącu')
month = st.checkbox('rodzaju miesiąca (np. wszystkie stycznie)')
day = st.checkbox('rodzaju dnia tygodni (np. poniedziałki)')
hour = st.checkbox('godzinie')
st.write('Dopiero po wybraniu wszystkich interesujących Cię opcji naciśnij "Compute"')
compute = st.button('Compute')

if file is not None:    
    if compute:        
        fun = data_preprocessing(file)
        df = fun[0]
        days_counter = datetime.date.today() - df['time'].iloc[-1]
        st.write('Od', df['time'].iloc[-1], 'zobaczyłxś',fun[1], 'filmów, co daje ', int(fun[1]/(days_counter.days)), 'zobaczonych filmów dziennie')
        st.write('Najczęściej oglądane kanały')
        st.write(df['channel'].value_counts())

        if channel in df['channel'].unique():            
                df = df[df['channel']==channel]     

        if top_video:
                st.write('Najczęściej oglądane wideo')
                st.write(df['wideo'].value_counts())
        if year:
            st.write('Liczba wyświetleń wideo w danym roku')
            st.bar_chart(df['year'].value_counts())

        if year_month:
            st.write('Liczba wyświetleń wideo w danym miesiącu')
            st.bar_chart(df['year_month'].value_counts())

        if month:
            st.write('Liczba wyświetleń wideo w danym rodzaju miesiąca')
            st.bar_chart(df['month'].value_counts())

        if day:
            st.write('Liczba wyświetleń wideo w danym dniu tygodnia (poniedziałek = 0)')
            st.bar_chart(df['day_of_week'].value_counts())
        if hour:
            st.write('Liczba wyświetleń wideo w danej godzinie')
            st.bar_chart(df['hour'].value_counts())
