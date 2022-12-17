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
st.write('Przed włączeniem obliczeń ustaw wszystkie preferowane filrty a następnie naciśnij przycisk Compute')
channel = st.text_input('','Wybierz kanał, którego statystyki oglądania chcesz wyświetlić')
begin = st.date_input('Wprowadź datę od której chcesz wyświetlać statystki')
end = st.date_input('Wprowadź datę końcową do której chcesz wyświetlać statystyki')
compute = st.button('Compute')


if file is not None:     
    
    if compute:        
        df = data_preprocessing(file)        
        st.write(df.columns)
        st.write(df.head(3))

        if begin != 'Wprowadź datę od której chcesz wyświetlać statystki' and end != 'Wprowadź datę końcową do której chcesz wyświetlać statystyki':
            df = df[(df['time']>begin) & (df['time']<end)]

        if channel == 'Wybierz kanał, którego statystyki oglądania chcesz wyświetlić':
            st.write('Najczęściej oglądane wideo')
            st.write(df['wideo'].value_counts())
            st.write('Najczęściej oglądane kanały')
            st.write(df['subtitles'].value_counts())
        else:
            st.write('Dane dla',channel)
            df = df[df['subtitles']==channel]
            st.write('Najczęściej oglądany film kanału',channel)
            st.write(df['wideo'].value_counts())
    else:
        pass





