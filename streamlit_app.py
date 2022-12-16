import pandas as pd
import os,json
import streamlit as st

pd.options.mode.chained_assignment = None
st.title('LSowa analiza')

"""
# Dzieeeeeeeeeń dobry

Stworzyłem tą aplikację po to, aby odpowiedzieć na pytani, których nigdy nawet nie zadaliście.

Aby poddać analizie waszą historię YT musicie dysponować 
[plikiem w formacie JSON zawierający waszą historię oglądania](https://www.youtube.com/watch?v=zlzzO1e6dws)
"""

def data_preprocessing():
    df = pd.DataFrame()
    pwd = os.getcwd()
    files = [x for x in os.listdir(pwd) if '.json' in x]

    for file in files:
        with open(pwd + '/' + file,'r',encoding='utf-8') as f:
            data = json.loads(f.read())
            df_new_row = pd.DataFrame(pd.json_normalize(data))
            df = pd.concat([df,df_new_row])

    
    df = df.drop(['products','activityControls','description','details'], axis = 1)
    len_1 = len(df)
    df = df.dropna()
    len_2 = len(df)
    df['hour'] = df['time']
    df['day_of_week'] = pd.DatetimeIndex(df['time']).day_of_week
    df['year'] = pd.DatetimeIndex(df['time']).year
    df['month'] = pd.DatetimeIndex(df['time']).month
    df['year_month'] = df['time']

    print('As a result of deleting damaged entries,', len_1-len_2, 'information about videos have been lost')
    print('Converting json file into df are processing. Be patient, this process may take up to 2-3 minutes')

    for item in range(len(df)):
        df['subtitles'].iloc[item] = df['subtitles'].iloc[item][0]['name']
        df['hour'].iloc[item] = df['time'].iloc[item][11:13]
        df['year_month'].iloc[item] = df['time'].iloc[item][:7]
        df['time'].iloc[item] = df['time'].iloc[item][:10]

    
    
    return df
df = data_preprocessing()

top_channels = df['subtitles'].value_counts()
top_videos = df['title'].value_counts()
top_ls = df['title'][df['subtitles']=='Lekko Stronniczy'].value_counts()

print('Most watched videos of all time:')
print()
print(top_videos.head(10))
print()

print('Most watched channels of all time')
print()
print(top_channels.head(20))
print()

print('Most watched LS videos of all time')
print()
print(top_ls.head(20))
