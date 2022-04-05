# import
import streamlit as st
from datetime import date

import yahoo_finance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from  plotly import graph_obj as go


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


st.title("I Stocke prediction appication")


stocks = ("AAPL", "GOOG", "MSFT", "TSLA")
selected_stocks = st.selectbox("Select stocks fro prediction", stocks)

n_years = st.slider("Yers of prediction: ", 1,4)
period = n_years * 365


def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text("load data...")

data = load_data(selected_stocks)
data_load_state.text("loading done")

st.subheader('Raw data')
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name= 'Stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['close'], name= 'Stock_close'))
    fig.layout.update(title_text="Time series data", xaxis_rangelider_visible = True)
    st.plotly_chart(fig)


plot_raw_data()

#forecast

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())


st.write('Forecast data')
fig1 = plot_plotly(m, forecast)

st.plotly_chart(fig1)

st.write('Forecast component')
fig2= m.plot_components(forecast)
st.write(fig2)
