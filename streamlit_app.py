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
        st.write(df.head(10))

        
        

    
    
    return df





df = data_preprocessing()



