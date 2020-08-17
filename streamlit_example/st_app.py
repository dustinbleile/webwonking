import streamlit as st
import numpy as np
import pandas as pd


# Apps run top to bottom and re-execute on any changes
# Run flow with:
#   streamlit run st_app.py

st.title("gene expr explorer")

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.write("## Add more stuff")

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

option_tens = st.sidebar.selectbox(
    'Which number do you like best?',
     df['second column'])

'You selected:', option