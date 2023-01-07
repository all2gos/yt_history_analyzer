import pandas as pd
import streamlit as st
import datetime
import numpy as np
import seaborn as sns


pd.options.mode.chained_assignment = None
st.set_page_config(page_title='yt_analyzer', page_icon=':mag:')
st.title('LSowa analiza')


"""
## Dzieeeeeeeeeń dobry

Stworzyłem tę aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON z historią oglądania](https://youtu.be/OMc7w1DinPM?t=804)

"""


"""

### Trwa przerwa techniczna
-----------------------------------------------------------------------------------------------
#### Aktualizacja 4.01.2023
###### Dodanie możliwości wyboru specyficznego okresu poddawanego analizie

###### Plany:
###### Dodanie możliwości wyboru kilku kanałów żeby porównywać ich statystyki między sobą

###### Wszelkie bugi można zgłaszać korzystając z opcji z menu w prawym górnym rogu. Będe wzdzięczny za każdy feedback
-------------------------------------------------------------------------------------------------
"""

"""
#### Właściwy program
"""
def data_preprocessing(file):
    df = pd.read_json(file)  
    df['hour'] = df['time']
    df['day_of_week'] = pd.DatetimeIndex(df['time']).day_of_week
    df['year'] = pd.DatetimeIndex(df['time']).year
    df['month'] = pd.DatetimeIndex(df['time']).month
    df['year_month'] = df['time']
    df['wideo'] = df['time']    
    df['channel'] = df['subtitles']
    st.write('Konwertowanie pliku JSON trwa. Proszę o cierpliwość ten proces może trwać nawet kilka minut')   
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
channel_menu = st.checkbox('Zaznacz, jeśli chcesz sprawdzić statystyki dla konkretnego kanału')
if channel_menu:    
    channel = st.text_input('','Wpisz nazwe kanału (uwaga na literówki)').split(',')
    st.write('Jeżeli wpiszesz kanał, który nie występuje w Twojej historii wówczas statystyki dalej będą wyświetalne dla wszystkich kanałów')

data_choice = st.checkbox('Zaznacz jeśli chcesz sprawdzić statystyki dla specyficznego okresu')

if data_choice:
    begin = st.date_input('Data początkowa')
    end = st.date_input('Data końcowa')

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
        try:  
            is_date_exist = begin
            pre_data_df= fun[0]
            df = []  
            for i in range(len(pre_data_df)):
                if pre_data_df['time'].iloc[i]>begin and pre_data_df['time'].iloc[i]<end:
                    df.append(pre_data_df.iloc[i])
            df = pd.DataFrame(data=df, columns = pre_data_df.columns)
            st.write('Od', begin, 'do', end, 'zobaczyłxś',len(df), 'filmów, co daje ', int(len(df)/(end-begin).days), 'zobaczonych filmów dziennie')

        except:
            pass        
        days_counter = datetime.date.today() - df['time'].iloc[-1]
        try:
            is_date_exist = begin
        except:            
            st.write('Od', df['time'].iloc[-1], 'do', df['time'].iloc[0],'zobaczyłxś',fun[1], 'filmów, co daje ', int(fun[1]/(days_counter.days)), 'zobaczonych filmów dziennie')
        st.write('Najczęściej oglądane kanały w podanym okresie')
        st.write(df['channel'].value_counts())
        spelling_counter = 0
        
        try:
            for char in channel:
                if char in df['channel'].unique():
                    spelling_counter +=1
            
            if spelling_counter == len(channel):
                filtered_df = pd.DataFrame(data = [], columns = df.columns)
                for i in range(len(channel)):
                    part_df = df[df['channel'] == channel[i]]
                    filtered_df = pd.concat([filtered_df,part_df])
                df = filtered_df
            else:
                st.write('Coś jest nietak we wpisanych kanałach. Zostaną wyświetlone statystyki dla wszystkich kanałów')     
        except:
            pass
        if top_video:
                st.write('Najczęściej oglądane wideo')

                st.write(df['wideo'][df['wideo'] != 'film, który został usunięty'].value_counts())

                
        if year:
            st.write('Liczba wyświetleń wideo w danym roku')   
            sns.countplot(df['year'],hue='channel')

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
