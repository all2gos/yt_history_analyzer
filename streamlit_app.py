import pandas as pd
import streamlit as st
import datetime


pd.options.mode.chained_assignment = None
st.title('LSowa analiza')

"""
## Dzieeeeeeeeeń dobry

Stworzyłem tę aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON z historią oglądania](https://www.youtube.com/watch?v=zlzzO1e6dws)

"""
def data_preprocessing(file):
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
        df['time'].iloc[item] = datetime.datetime(int(df['time'].iloc[item][:4]),int(df['time'].iloc[item][5:7]),int(df['time'].iloc[item][8:]))     
    return df

file = st.file_uploader("Tutaj wklej swoją historię")
channel = st.text_input('','Wybierz kanał, którego statystyki oglądania chcesz wyświetlić, możesz zostawić to pole puste')
top_video = st.checkbox('Zaznacz, jeśli chcesz zobaczyć najczęściej oglądane filmy')

year = st.checkbox('Zaznacz, jeśli chcesz zobaczyć liczbę filmów w zależności od roku')
year_month = st.checkbox('Zaznacz, jeśli chcesz zobaczyć liczbę filmów w zależności od miesiąca')
day = st.checkbox('Zaznacz, jeśli chcesz zobaczyć liczbę filmów w zależności od rodzaju dnia tygodni (np. poniedziałki)')
hour = st.checkbox('Jak wyżej tylko godziny')
month = st.checkbox('Jak wyżej tylko miesiące')
compute = st.button('Compute')

if file is not None:    
    if compute:        
        df = data_preprocessing(file) 

        if channel == 'Wybierz kanał, którego statystyki oglądania chcesz wyświetlić, możesz zostawić to pole puste' or channel == '':
            if top_video:
                st.write('Najczęściej oglądane wideo')
                st.write(df['wideo'].value_counts())
            st.write('Najczęściej oglądane kanały')
            st.write(df['subtitles'].value_counts())
        else:
            st.write('Dane dla',channel)
            df = df[df['subtitles']==channel]
            if top_video:
                st.write('Najczęściej oglądany film kanału',channel)
                st.write(df['wideo'].value_counts())
        
        if year:
            st.write('Liczba wyświetleń wideo w danym roku')
            st.bar_chart(df['year'].value_counts())

        if year_month:
            st.write('Liczba wyświetleń wideo w danym miesiącu')
            st.bar_chart(df['year_month'].value_counts())
        if day:
            st.write('Liczba wyświetleń wideo w danym dniu tygodnia (poniedziałek = 0)')
            st.bar_chart(df['day_of_week'].value_counts())
        if hour:
            st.write('Liczba wyświetleń wideo w danej godzinie')
            st.bar_chart(df['hour'].value_counts())

        if month:
            st.write('Liczba wyświetleń wideo w danym rodzaju miesiąca')
            st.bar_chart(df['month'].value_counts())
        
    else:
        pass




