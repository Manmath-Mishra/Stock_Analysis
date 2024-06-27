import pandas as pd
import yfinance as yf
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import numpy as np
import streamlit as st

def scrap_headlines(ticker):
    
    articles=[]
    for news in ticker.news:
        articles.append([news['link'],news['title']])
    return articles


def Home():
     
    st.title('Stock Market Analysis Dashboard')

    # Text input for stock ticker
    ticker = st.text_input('Enter Stock Ticker', 'AAPL')
    try:
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
        st.subheader("Statistics")
        col1,col2,col3,col4= st.columns(4)
        with col1:
            st.dataframe(st_data[['Open']].agg(['min','max','mean','median']),width=1920)

        with col2:
            st.dataframe(st_data[['Close']].agg(['min','max','mean','median']),width=1920)
        
        with col3:
            st.dataframe(st_data[['High']].agg(['min','max','mean','median']),width=1920)

        with col4:
            st.dataframe(st_data[['Low']].agg(['min','max','mean','median']),width=1920)
        st.header(':orange[Graphs]')
        
        fig = px.line(st_data, x=st_data.index, y=['Close','Open'], title=f"{st_info['shortName']} Closing & Opening Prices",markers=True)
        fig.update_yaxes(title_text=f"Prices(Close and Open) ({st_info['financialCurrency']})")
        st.plotly_chart(fig,use_container_width=True)

        st.divider()
        st.header(f":orange[Financial News ({st_info['shortName']})]")
        articles= scrap_headlines(stock)
        if (len(articles)==0):
            st.error("Sorry unable to procure news")
        for i in range(len(articles)):
            col1,col2 = st.columns([0.9,0.1])
            with col1:
                st.subheader(f'{i+1}.{articles[i][1]}')
            with col2:
                st.page_link(articles[i][0],label=":blue[Read More...]")
    except Exception as e:

        st.error("No such Ticker available!")
       

def Calculator():
    st.title('Page under construction!!')    

pages = {
    "Home📈": Home,
    "Calculator🔢":Calculator
    
}
st.set_page_config(
        page_title="Stock Predicter",
        page_icon="📈",
        layout="wide",
    )
st.sidebar.title("Navigation")
selection=st.sidebar.radio("Pages",list(pages.keys()),index=0)
pages[selection]()

