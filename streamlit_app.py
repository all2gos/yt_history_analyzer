import pandas as pd
import streamlit as st
import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


pd.options.mode.chained_assignment = None
st.set_page_config(page_title='yt_analyzer', page_icon=':mag:')
st.title('Analiza historii oglądania YT')


"""
## Dzieeeeeeeeeń dobry

Stworzyłem tę aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON z historią oglądania](https://youtu.be/OMc7w1DinPM?t=804)

"""
"""
#### Aktualizacji 26.02.2023
###### Poprawienie responsywności strony (pierwsze i nie ostatnie)
###### Dodanie paska postępu

-----------------------------------------------------------------------------------------------
###### Coś nie działa? Masz sugestie co mogę poprawić? Pisz śmiało na stottkoraf@gmail.com
-------------------------------------------------------------------------------------------------
"""

"""
#### Właściwy program
"""
def data_preprocessing(file):
    percent_complete = 0
    my_bar = st.progress(0)

    df = pd.read_json(file)  
    df = df.assign(day_of_week= lambda x: pd.DatetimeIndex(x.time).day_of_week,year= lambda x: pd.DatetimeIndex(x.time).year,
              month= lambda x: pd.DatetimeIndex(x.time).month,wideo = lambda x: x.title,year_month = lambda x: x.time,
              hour = lambda x: x.time, channel = lambda x: x.subtitles)
    print('Generowanie statystyk trwa. Proszę o cierpliwość ten proces może trwać nawet kilka minut')   
    list_of_nan = 0

    df['year_month'] = df['year_month'].map(lambda x: x[2:7])
    df['hour'] = df['hour'].map(lambda x: x[11:13])
    df['time'] = df['time'].map(lambda x: datetime.date(int(x[:4]),int(x[5:7]),int(x[8:10])))
    df['wideo'] = df['wideo'].map(lambda x: x[11:])

    for item in range(len(df)):
        try:
            df['channel'].iloc[item] = df['channel'].iloc[item][0]['name']
        except:
            list_of_nan+=1

        if item % int(len(df)/100)==0:   
            percent_complete+=1
            if percent_complete<101:              
                my_bar.progress(percent_complete) 

    df['channel'] = df['channel'].map(lambda x: 'sanah' if x=='sanahVEVO' else x)
    df['channel'] = df['channel'].map(lambda x: 'Dobrzewiesz Nagrania' if x=='Pistacho95ldz' else x)

    st.write('W wyniku usuwania uszkodzonych informacji,', list_of_nan, 'pozycji z historii zostało usuniętych')
    return df, len(df)

file = st.file_uploader("Tutaj wklej swoją historię")

st.write('Wybierz jakie statystyki chcesz zobaczyć')

top_channel = st.checkbox('Najczęściej oglądane kanały')
top_video = st.checkbox('Najczęściej oglądane filmy')

st.write('Liczbę filmów zobaczonych w danym:')
year = st.checkbox('roku')
year_month = st.checkbox('miesiącu')
month = st.checkbox('rodzaju miesiąca (np. wszystkie stycznie)')
day = st.checkbox('rodzaju dnia tygodni (np. poniedziałki)')
hour = st.checkbox('godzinie')

"""
-------------------------------------------------------------------------------------------------
#### Zaawansowane filtrowanie
"""

channel_menu = st.checkbox('Zaznacz, jeśli chcesz sprawdzić statystyki dla konkretnych kanałów')
if channel_menu:    
    st.write('W przypadku wpisywania większej liczby kanałów należy robić to bez żadnych spacji (chyba, że spacje występują w nazwie kanału), oddzielając poszczególne kanały przecinkiem np. "Lekko Stronniczy,sanah,Ziemniak"')
    channel = st.text_input('','Wpisz nazwe kanałów (uwaga na literówki)').split(',')
    st.write('Jeżeli wpiszesz kanał, który nie występuje w Twojej historii wówczas statystyki dalej będą wyświetalne dla wszystkich kanałów')
video_menu = st.checkbox('Zaznacz jeśli chcesz sprawdzić statystyki dla konkretnych wideo')
if video_menu:
    st.write('W przypadku wpisywania większej liczby wideo należy robić to bez żadnych spacji (chyba, że spacje występują w tytule wideo), oddzielając poszczególne kanały średnikiem np. "Nie Kłami;Ed Sheeran - Give Me Love (Official Music Video)" Polecam wyświetlić sobie top oglądane wideo, a następnie do notatki gdzieś przeklejać dokładne nazwy. To bardzo toporne - wiem, dlatego jest w planach wprowadzenie wyświetlania najpopularniejszych wideo w danym okresie, a ta opcja zostanie typowo do śledzenia historii jednego, może dwóch wideo naraz')
    video = st.text_input('','Wpisz nazwe kanałów (uwaga na literówki)').split(';')
data_choice = st.checkbox('Zaznacz jeśli chcesz sprawdzić statystyki dla specyficznego okresu')

if data_choice:
    begin = st.date_input('Data początkowa')
    end = st.date_input('Data końcowa')
mark = st.checkbox('Zaznacz jeśli chcesz, żeby nad każdą kolumną w wykresie była wyświetlona wartość liczbowa')

"""
-------------------------------------------------------------------------------------------------

"""
st.write('Dopiero po wybraniu wszystkich interesujących Cię opcji naciśnij "Compute"')
compute = st.button('Compute')

if file is not None:    
    if compute:        
        fun = data_preprocessing(file)        
        df = fun[0]   
        st.write(df)     
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
        
        if top_channel:
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

        try:
            for char in video:
                if char in df['wideo'].unique():
                    spelling_counter +=1
            if spelling_counter == len(video):
                filtered_df = pd.DataFrame(data = [], columns = df.columns)
                for i in range(len(video)):
                    part_df = df[df['wideo'] == video[i]]
                    filtered_df = pd.concat([filtered_df,part_df])
                df = filtered_df
                
            else:
                st.write('Coś jest nietak we wpisanych wideo. Zostaną wyświetlone statystyki dla wszystkich kanałów')     
        except:
            pass

        if top_video:
                st.write('Najczęściej oglądane wideo')

                st.write(df['wideo'][df['wideo'] != 'film, który został usunięty'].value_counts())
        var = None
        title = ''
        try:
            if video:
                var = 'wideo'
                title = 'wideo'
        except:
            try:
                if channel:
                    var = 'channel'    
                    title = 'Kanały'
            except:
                pass 
        if year:            
            fig = plt.figure(figsize=(10,4))             
            ax = sns.countplot(data=df, x='year', hue = var)   
            ax.legend(title=title)  
            ax.set_title('Liczba wyświetleń w zależności od roku')
            ax.set_ylabel('Liczba odtworzeń')
            ax.set_xlabel('Rok')   
            if mark:     
                for container in ax.containers:
                    ax.bar_label(container)
            st.pyplot(fig)

        if year_month:
            fig = plt.figure(figsize=(20,4))    
            plt.tight_layout()         
            ax = sns.countplot(data=df, x='year_month', hue = var)   
            ax.legend(title=title)  
            ax.set_title('Liczba wyświetleń w zależności od miesiąca')
            ax.set_ylabel('Liczba odtworzeń')
            ax.set_xlabel('Miesiąc')  
            if mark:      
                for container in ax.containers:
                    ax.bar_label(container)
            st.pyplot(fig)

        if month:
            fig = plt.figure(figsize=(10,4))             
            ax = sns.countplot(data=df, x='month', hue = var)   
            ax.legend(title=title)  
            ax.set_title('Liczba wyświetleń w zależności od rodzaju miesiąca')
            ax.set_ylabel('Liczba odtworzeń')
            ax.set_xlabel('Rodzaj miesiąca')  
            if mark:      
                for container in ax.containers:
                    ax.bar_label(container)
            st.pyplot(fig)

        if day:
            fig = plt.figure(figsize=(10,4))             
            ax = sns.countplot(data=df, x='day_of_week', hue = var)   
            ax.legend(title=title)  
            ax.set_title('Liczba wyświetleń w zależności od dnia tygodnia (poniedziałek = 0)')
            ax.set_ylabel('Liczba odtworzeń')
            ax.set_xlabel('Dzień tygodnia')            
            if mark:     
                for container in ax.containers:
                    ax.bar_label(container)
            st.pyplot(fig)
        if hour:
            fig = plt.figure(figsize=(10,4))             
            ax = sns.countplot(data=df, x='hour', hue = var)   
            ax.legend(title=title)  
            ax.set_title('Liczba wyświetleń w zależności od godziny')
            ax.set_ylabel('Liczba odtworzeń')
            ax.set_xlabel('Godzina')  
            if mark:      
                for container in ax.containers:
                    ax.bar_label(container)
            st.pyplot(fig)
