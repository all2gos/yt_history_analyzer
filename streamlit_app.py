import pandas as pd
import os,json
import streamlit as st

pd.options.mode.chained_assignment = None
st.title('LSowa analiza')

"""
## Dzieeeeeeeeeń dobry

Stworzyłem tą aplikację po to, aby odpowiedzieć na pytania, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON zawierający waszą historię oglądania](https://www.youtube.com/watch?v=zlzzO1e6dws)
"""

def data_preprocessing():
    
    df = pd.DataFrame()
    file = st.file_uploader("Choose a file")
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

        st.write('As a result of deleting damaged entries,', len_1-len_2, 'information about videos have been lost')
        st.write('Converting json file into df are processing. Be patient, this process may take up to 2-3 minutes')

        for item in range(len(df)):
            df['subtitles'].iloc[item] = df['subtitles'].iloc[item][0]['name']
            df['hour'].iloc[item] = df['time'].iloc[item][11:13]
            df['year_month'].iloc[item] = df['time'].iloc[item][:7]
            df['time'].iloc[item] = df['time'].iloc[item][:10]

    
    
    return df

df = data_preprocessing()

st.write(df.head(10))
