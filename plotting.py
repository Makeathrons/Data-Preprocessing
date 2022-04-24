import streamlit as st  # steramlit for ui
import pandas as pd  # pandas for data handling
import plotly.express as px  # plotly for graph plotting
import base64
from io import StringIO, BytesIO 

# Downoad link for html graph download
def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)


st.set_page_config(page_title='Makeathon Plotter')
st.title('Data plotter from Excel file')
st.subheader('Upload your Excel file')

# Uploaded file
uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')

if uploaded_file:
    # Reading the uploaded file
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)

    # X-AXIS 
    groupby_column = st.selectbox(
        'What would you like to analyse? (x-axis)',
        df.columns
    )

    # Y-AXIS
    output_column = st.selectbox(
        'What column would you like to plot ? (y-axis)',
        df.columns
    )
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_column].sum()

    # Plot the data
    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y=output_column,
        color=output_column,
        color_continuous_scale=['red', 'yellow', 'green', 'purple'],
        template='plotly_white',
        title=f'<b>{output_column} by {groupby_column}</b>'
    )
    st.plotly_chart(fig)

    # Download plotted graph
    st.subheader('Download your graph:')
    generate_html_download_link(fig)