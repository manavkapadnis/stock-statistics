import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import trendet
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import regex as re
import webbrowser


sns.set(style='darkgrid')
import investpy

st.markdown(
    """
<style>
.sidebar .sidebar-content {
    color: #000;
    background-color:   #4267B2;
}
</style>
""",
  unsafe_allow_html=True,
)
st.sidebar.subheader('About the Creator:')
st.sidebar.markdown('Manav Nitin Kapadnis')
st.sidebar.markdown('Sophomore | IIT Kharagpur')

github_url = 'https://github.com/manavkapadnis'
if st.sidebar.button('Github'):
    webbrowser.open_new_tab(github_url)

linkedin_url = 'https://www.linkedin.com/in/manav-nitin-kapadnis-013b94192/'
if st.sidebar.button('LinkedIn'):
    webbrowser.open_new_tab(linkedin_url)

k_url = 'https://www.kaggle.com/darthmanav'
if st.sidebar.button('Kaggle'):
    webbrowser.open_new_tab(k_url)


st.title("Company Stock Statistics")

menu=['Cenkos Securities',"Finncap Group", "Mattioli Woods",'Draper Esprit']
choice = st.sidebar.selectbox("Select the company",menu)

para_cenkos = "Cenkos Securities PLC offers institutional securities services. The Company advises on corporate finance, offers corporate broking, institutional stockbroking, institutional sales and market making services, and manages investment funds"
para_harwood = "Harwood Wealth Management Group plc operates as a wealth management firm. The Company provides financial planning and wealth management services. Harwood Wealth Management Group serves customers in the United Kingdom."
para_panmure = "Panmure Gordon & Co. is a British corporate and institutional investment bank. The firm works with growth and mid-size companies. Its businesses are: investment banking, equities, including research and institutional sales and trading, and prime services."
para_finncap = "finnCap Ltd is a British investment bank and a corporate and institutional stockbroker, based in London. It operates in four areas of business: investment banking, equities research, institutional sales and trading, and market making."
para_mattioli = "Mattioli Woods is a leading provider of wealth management and employee benefit services with multiple offices throughout the UK, including; Leicester, Aberdeen, Belfast, Birmingham, Buckingham, Edinburgh, Glasgow, London, Manchester, Newmarket and Preston."
para_draper = "Draper Esprit is a venture capital firm, with offices in London, Cambridge and Dublin. Investing in high growth technology companies with global ambitions.The company invests across four sectors: Consumer, Digital Health & Wellness, AI, Deeptech & Hardware & Cloud, Enterprise & SaaS, Draper Esprit has also developed a FinTech investment thesis as the company invests in the future of financial services."

def plot_time_series(stock):
    df_ticker = yf.download(stock, period='max')
    data = df_ticker.sort_index(ascending=True, axis=0)
    data['Date'] = data.index
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.Date, y=data['Open'], name="stock_open",line_color='crimson'))
    fig.add_trace(go.Scatter(x=data.Date, y=data['Close'], name="stock_close",line_color='dimgray'))
    fig.add_trace(go.Scatter(x=data.Date, y=data['High'], name="stock_high",line_color='blueviolet'))
    fig.add_trace(go.Scatter(x=data.Date, y=data['Low'], name="stock_low",line_color='darksalmon'))

    fig.layout.update(title_text='Stock Price with Rangeslider',xaxis_rangeslider_visible=True, template='plotly_dark')
    st.plotly_chart(fig)

def show_statistics(ticker,paragraph_about_company, CompanyName):
  df_ticker = yf.Ticker(ticker)
  sector = df_ticker.info['sector']
  prevClose = df_ticker.info['previousClose']
  marketCap = df_ticker.info['marketCap']
  twoHunDayAvg = df_ticker.info['twoHundredDayAverage']
  fiftyTwoWeekHigh = df_ticker.info['fiftyTwoWeekHigh']
  fiftyTwoWeekLow = df_ticker.info['fiftyTwoWeekLow']
  Name = df_ticker.info['longName']
  averageVolume = df_ticker.info['averageVolume']
  shortRatio = df_ticker.info['shortRatio']
  ftWeekChange = df_ticker.info['52WeekChange']
  website = df_ticker.info['website']
  business_sumary = df_ticker.info['longBusinessSummary']
  payoutRatio = df_ticker.info['payoutRatio']
  regularMarketDayHigh = df_ticker.info['regularMarketDayHigh']
  regularMarketDayLow = df_ticker.info['regularMarketDayLow']
  fiveYearAvgDividendYield = df_ticker.info['fiveYearAvgDividendYield']
  fiftyDayAverage = df_ticker.info['fiftyDayAverage']

  st.subheader(Name)
  st.write(business_sumary)
  st.write("\n The following information contains different insights about the Company Stock")

    #st.write('Company Name -', Name)
  st.write('Sector -', sector)
  st.write('Company Website -', website)
  st.write('Average Volume -', averageVolume)
  st.write('Market Cap -', marketCap)
  st.write('Previous Close -', prevClose)
  st.write('Regular Market Day High -', regularMarketDayHigh)
  st.write('Regular Market Day Low -', regularMarketDayLow)
  st.write('52 Week Change -', ftWeekChange)
  st.write('52 Week High -', fiftyTwoWeekHigh)
  st.write('52 Week Low -', fiftyTwoWeekLow)
  st.write('50 Day Average - ',fiftyDayAverage)
  st.write('200 Day Average -', twoHunDayAvg)
  st.write('Short Ratio -', shortRatio)
  st.write('Pay Out Ratio -', payoutRatio)
  st.write('Five Year Average Dividend Yield - ', payoutRatio)
  plot_time_series(ticker)

def meeting_date_statistics(stock_ticker,date_start,date_end):
  df = trendet.identify_all_trends(stock=stock_ticker,
                                 country='united kingdom',
                                 from_date=date_start,
                                 to_date=date_end,
                                 window_size=7,
                                 identify='both')

  df.reset_index(inplace=True)
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'],mode='lines+markers',name = 'No trend'))
  labels = df['Up Trend'].dropna().unique().tolist()

  for label in labels:
      fig.add_trace(go.Scatter(x=df[df['Up Trend'] == label].Date,
                   y=df[df['Up Trend'] == label]['Close'],name='Up Trend',
                   line = dict(color='green'),mode='lines+markers'))

  labels = df['Down Trend'].dropna().unique().tolist()

  for label in labels:
      fig.add_trace(go.Scatter(x=df[df['Down Trend'] == label].Date,
                   y=df[df['Down Trend'] == label]['Close'],line = dict(color='red'), name = 'Down Trend',mode='lines+markers',))

  fig.update_layout(template='plotly_dark',xaxis_rangeslider_visible=True)
  st.plotly_chart(fig)

def change_date(date_streamlit, months=2):
  year,month,day = re.split('-',str(date_streamlit))
  date_input_function = day +'/'+ month +'/'+year
  if((int(month)+months)%12==0):
    date_end_function = day+'/'+str(12) +'/'+year
  else:
    date_end_function = day+'/'+str((int(month)+months)%12) +'/'+year
    
  today = date.today()
  d3 = today.strftime("%d/%m/%y")

  if((int(month)+months)%12==0):
    if(datetime(int(year),int(day),12)<datetime.today()):
      date_end_function= d3
  else:
    if(datetime(int(year),int(day),(int(month)+months)%12)<datetime.today()):
      date_end_function= d3

  day,month,year = re.split('/',str(date_end_function))

  date_end_function = day +'/'+ month +'/'+'20'+year

  return date_input_function,date_end_function

if choice == "Cenkos Securities":
  show_statistics('CNKS.L',para_cenkos,"Cenkos Securities")
  date = st.date_input("Pick a Meeting date:")
  #print(date)
  #date_start,date_end  = change_date(date,2)
  #meeting_date_statistics('CNKS',date_start,date_end)
#elif choice == "Harwood Wealth Management Group":

#elif choice == "Panmure Gordon":

elif choice == "Finncap Group":
  show_statistics('FCAP.L',para_finncap,"Finncap Group")
  date = st.date_input("Pick a Meeting date:")
  #date_start,date_end  = change_date(date,2)
  #meeting_date_statistics('FCAP',date_start,date_end)

elif choice == "Mattioli Woods":
  show_statistics('MTW.L',para_mattioli,"Mattioli Woods")
  date = st.date_input("Pick a Meeting date:")
  #date_start,date_end  = change_date(date,2)
  #meeting_date_statistics('MTWL',date_start,date_end)

elif choice == 'Draper Esprit':
  show_statistics('GRWXF',para_draper,"Draper Esprit")
  date = st.date_input("Pick a Meeting date:")
  #date_start,date_end  = change_date(date,2)
  #meeting_date_statistics('GROW',date_start,date_end)



