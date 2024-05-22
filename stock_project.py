import pandas as pd
import yfinance as yf
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import numpy as np
import streamlit as st

def scrap_headlines(ticker):
    URL="https://finance.yahoo.com/quote/"+ticker
    html_data= requests.get(URL).text
    soup= BeautifulSoup(html_data,'html.parser')
    articles=[]
    for data in soup.find_all('h3'):
        if(len(data.get('class','default'))>1):
            if(data.get('class','default')[1]=='svelte-1v1zaak'):
                if('gemini' not in data.parent.attrs['href'] ):
                    articles.append([data.parent.attrs['href'],data.text])
    return articles


def create_dashboard():
    
    st.title('Stock Market Analysis Dashboard')

    # Text input for stock ticker
    ticker = st.text_input('Enter Stock Ticker', 'AAPL')
    stock= yf.Ticker(ticker)
    st_data= stock.history(period="5d")
    st.info('Additional information')
    st_info = stock.info
    st.write("Full Name:-",st_info['longName'])
    st.write("Financial Currency:-",st_info['financialCurrency'])
    st.write("Current Price:-",st_info['currentPrice'])
    st.write("Country:-",st_info['country'])
    st.write("Website:-",st_info['website'])
    st.write("Summary:-",st_info['longBusinessSummary'],"\n")

    st.subheader("Previous 5 day analysis")
    st.dataframe(st_data,width=1920)
    st.write("\n")
    st.header(':orange[Graphs]')
    
    col1,col2 = st.columns(2,gap="large")
    with col1:
        fig = px.line(st_data, x=st_data.index, y='Close', title=f"{st_info['shortName']} Closing Prices",markers=True)
        fig.update_yaxes(title_text=f"Closing Prices ({st_info['financialCurrency']})")
        st.plotly_chart(fig)
    with col2:
        fig = px.line(st_data, x=st_data.index, y='Open', title=f"{st_info['shortName']} Opening Prices",markers=True)
        fig.update_yaxes(title_text=f"opening Prices ({st_info['financialCurrency']})")
        st.plotly_chart(fig)



    st.divider()
    st.header(f":orange[Financial News ({st_info['shortName']})]")
    articles= scrap_headlines(ticker)
    if (len(articles)==0):
        st.error("Sorry unable to procure news")
    for i in range(len(articles)):
        col1,col2 = st.columns([0.9,0.1])
        with col1:
            st.subheader(f'{i+1}.{articles[i][1]}')
        with col2:
            st.page_link(articles[i][0],label=":blue[Read More...]")
    
create_dashboard()
