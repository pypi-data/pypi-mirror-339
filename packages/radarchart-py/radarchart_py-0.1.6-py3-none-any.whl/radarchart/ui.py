import streamlit as st
import pandas as pd
from radarchart import plot


st.title("Radar Chart")

st.subheader('Step 1: Choose a CSV file')

uploaded_file = st.file_uploader('Choose a CSV file')
if uploaded_file is None:
    st.stop()

# Can be used wherever a "file-like" object is accepted:
df = pd.read_csv(uploaded_file, index_col=0)
with st.expander('CSV file'):
    st.dataframe(df)

df_ = df.copy()

st.subheader('Step 2: Customize the Radar Chart')

columns = st.multiselect('Column filter', options=df.columns)
if len(columns) > 0:
    df_ = df_.reindex(columns, axis=1)

index = st.multiselect('Row filter', options=df.index)
if len(index) > 0:
    df_ = df_.reindex(index)

norm_max = st.checkbox('Normalize', True)

fig, ax = plot(df_, norm_max=norm_max, streamlit=True)
st.write(fig)

st.dataframe(df_)
